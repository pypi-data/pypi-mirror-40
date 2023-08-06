import abc
import logging
from functools import wraps
import traceback
import aioamqp
import asyncio
from typing import Any, Dict, Type, Callable, Coroutine, Union
from json.decoder import JSONDecodeError
from easyqueue.queue import BaseJsonQueue
from easyqueue.exceptions import UndecodableMessageException, \
    InvalidMessageSizeException, MessageError


def _ensure_connected(coro: Callable[..., Coroutine]):
    @wraps(coro)
    async def wrapper(self: 'AsyncQueue', *args, **kwargs):
        retries = 0
        while self.is_running and not self.is_connected:
            try:
                await self.connect()
                break
            except Exception as e:
                await asyncio.sleep(self.seconds_between_conn_retry)
                retries += 1
                if self.logger:
                    self.logger.error({
                        'event': 'reconnect-failure',
                        'retry_count': retries,
                        'exc_traceback': traceback.format_tb(e.__traceback__)
                    })
        return await coro(self, *args, **kwargs)
    return wrapper


class AsyncQueue(BaseJsonQueue):
    def __init__(self,
                 host: str,
                 username: str,
                 password: str,
                 delegate_class: Type['AsyncQueueConsumerDelegate'] = None,
                 delegate: 'AsyncQueueConsumerDelegate' = None,
                 virtual_host: str = '/',
                 heartbeat: int = 60,
                 prefetch_count: int = 100,
                 max_message_length=0,
                 loop=None,
                 seconds_between_conn_retry: int = 1,
                 logger: logging.Logger=None):
        super().__init__(host, username, password, virtual_host, heartbeat)

        self.loop = loop or asyncio.get_event_loop()

        if delegate is not None and delegate_class is not None:
            raise ValueError("Cant provide both delegate and delegate_class")

        if delegate_class is not None:
            self.delegate = delegate_class(loop=self.loop, queue=self)
        else:
            self.delegate = delegate

        self.prefetch_count = prefetch_count

        if max_message_length < 0:
            raise ValueError("max_message_length must be a positive integer")

        self.max_message_length = max_message_length

        self._protocol = None  # type: aioamqp.protocol.AmqpProtocol
        self._transport = None  # type: asyncio.BaseTransport
        self._channel = None  # type: aioamqp.channel.Channel
        self.seconds_between_conn_retry = seconds_between_conn_retry
        self.is_running = True
        self.logger = logger
        self._connection_lock = asyncio.Lock()

    @property
    def connection_parameters(self):
        if self.delegate:
            on_error = self.delegate.on_connection_error
        else:
            on_error = None

        return {
            'host': self.host,
            'login': self.username,
            'password': self.password,
            'virtualhost': self.virtual_host,
            'loop': self.loop,
            'on_error': on_error,
            'heartbeat': self.heartbeat
        }

    @property
    def is_connected(self):
        # todo: This may not be enough
        return self._channel and self._channel.is_open

    async def connect(self):
        async with self._connection_lock:
            if self.is_connected:
                return

            conn = await aioamqp.connect(**self.connection_parameters)
            self._transport, self._protocol = conn
            self._channel = await self._protocol.channel()

    async def close(self):
        if not self.is_connected:
            return

        await self._protocol.close()
        self._transport.close()

    @_ensure_connected
    async def ack(self, delivery_tag: int):
        return await self._channel.basic_client_ack(delivery_tag)

    @_ensure_connected
    async def reject(self, delivery_tag: int, requeue=False):
        return await self._channel.basic_reject(delivery_tag=delivery_tag,
                                                requeue=requeue)

    @_ensure_connected
    async def put(self,
                  routing_key: str,
                  data: Any = None,
                  serialized_data: Union[str, bytes] = None,
                  exchange: str = ''):
        """
        :param data: A serializable data that should be serialized before
        publishing
        :param serialized_data: A payload to be published as is
        :param exchange: The exchange to publish the message
        :param routing_key: The routing key to publish the message
        """
        if data and serialized_data:
            raise ValueError("Only one of data or json should be specified")

        if data:
            serialized_data = self.serialize(data, ensure_ascii=False)

        if not isinstance(serialized_data, bytes):
            serialized_data = serialized_data.encode()

        return await self._channel.publish(payload=serialized_data,
                                           exchange_name=exchange,
                                           routing_key=routing_key)

    def _parse_message(self, body) -> Dict[str, Any]:
        if self.max_message_length:
            if len(body) > self.max_message_length:
                raise InvalidMessageSizeException(body)
        try:
            # todo: >>Serialize<< com tipo byte não tem o mesmo tratamento
            return self.deserialize(body)
        except TypeError:
            return self._parse_message(body.decode())
        except JSONDecodeError:
            raise UndecodableMessageException(
                '"{body}" can\'t be decoded as JSON'
                .format(body=body))

    async def _handle_callback(self, callback, **kwargs):
        """
        Chains the callback coroutine into a try/except and calls 
        `on_message_handle_error` in case of failure, avoiding unhandled 
        exceptions.
         
        :param callback: 
        :param kwargs: 
        :return: 
        """
        try:
            return await callback(**kwargs)
        except Exception as e:
            return await self.delegate.on_message_handle_error(handler_error=e,
                                                               **kwargs)

    async def _handle_message(self, channel, body, envelope, properties):
        """
        :rtype: asyncio.Task
        """
        tag = envelope.delivery_tag
        try:
            content = self._parse_message(body)
        except MessageError as e:
            callback = self._handle_callback(self.delegate.on_queue_error,
                                             body=body,
                                             delivery_tag=tag,
                                             error=e,
                                             queue=self)
        else:
            callback = self._handle_callback(self.delegate.on_queue_message,
                                             content=content,
                                             delivery_tag=tag,
                                             queue=self)
        return self.loop.create_task(callback)

    @_ensure_connected
    async def consume(self, queue_name: str, consumer_name: str = '') -> str:
        """
        :param queue_name: queue to consume
        :param consumer_name: Name to be used as a consumer identifier.
        :return: The consumer tag. Useful for cancelling/stopping consumption
        """
        # todo: Implement a consumer tag generator
        if not self.delegate:
            raise RuntimeError("Cannot start a consumer without a delegate")

        await self.delegate.on_before_start_consumption(queue_name, queue=self)
        await self._channel.basic_qos(prefetch_count=self.prefetch_count,
                                      prefetch_size=0,
                                      connection_global=False)
        tag = await self._channel.basic_consume(callback=self._handle_message,
                                                consumer_tag=consumer_name,
                                                queue_name=queue_name)
        return tag['consumer_tag']

    async def start_consumer(self):
        """ Coroutine that starts the connection and the queue consumption """
        await self.connect()
        consumer_tag = await self.consume(queue_name=self.delegate.queue_name)
        await self.delegate.on_consumption_start(consumer_tag, queue=self)

    async def stop_consumer(self, consumer_tag: str):
        if self._channel is None:
            raise ConnectionError("Queue isn't connected. "
                                  "Did you forgot to wait for `connect()`?")

        return await self._channel.basic_cancel(consumer_tag)


class AsyncQueueConsumerDelegate(metaclass=abc.ABCMeta):
    queue: AsyncQueue

    @property
    @abc.abstractmethod
    def queue_name(self) -> str:
        """ Name of the input queue to consume """
        raise NotImplementedError

    async def start(self):
        """ Coroutine that starts the connection and the queue consumption """
        await self.queue.start_consumer()

    async def on_before_start_consumption(self, queue_name: str,
                                          queue: 'AsyncQueue'):
        """
        Coroutine called before queue consumption starts. May be overwritten to
        implement further custom initialization.

        :param queue_name: Queue name that will be consumed
        :type queue_name: str
        :param queue: AsynQueue instanced
        :type queue: AsyncQueue
        """
        pass

    async def on_consumption_start(self,
                                   consumer_tag: str,
                                   queue: 'AsyncQueue'):
        """
        Coroutine called once consumption started.
        """

    @abc.abstractmethod
    async def on_queue_message(self, content, delivery_tag, queue):
        """
        Callback called every time that a new, valid and deserialized message
        is ready to be handled.

        :param delivery_tag: delivery_tag of the consumed message
        :type delivery_tag: int
        :param content: parsed message body
        :type content: dict
        :type queue: AsyncQueue
        """
        raise NotImplementedError

    async def on_queue_error(self, body, delivery_tag, error, queue):
        """
        Callback called every time that an error occurred during the validation
        or deserialization stage.

        :param body: unparsed, raw message content
        :type body: Any
        :param delivery_tag: delivery_tag of the consumed message
        :type delivery_tag: int
        :param error: THe error that caused the callback to be called
        :type error: MessageError
        :type queue: AsyncQueue
        """
        pass

    async def on_message_handle_error(self, handler_error: Exception,
                                      **kwargs):
        """
        Callback called when an uncaught exception was raised during message
        handling stage.

        :param handler_error: The exception that triggered
        :param kwargs: arguments used to call the coroutine that handled
        the message
        :return:
        """
        pass

    async def on_connection_error(self, exception: Exception):
        """
        Called when the connection fails
        """
        pass

