import aio_pika
import json

from config import (
    RABBITMQ_CONNECTION_STRING,
    RABBITMQ_QUEUE_NAME
)

from aio_pika.connection import Connection
from aio_pika.channel import Channel
from aio_pika.queue import ConsumerTag, Queue
from aio_pika.message import IncomingMessage
from typing import Any, Coroutine, Optional, Dict

AsyncFunction = Coroutine[Any, Any, Any]
ConsumerFunction = Coroutine[Any, Any, ConsumerTag]

async def boilderplate_consumer(message: IncomingMessage) -> None:
    await message.ack()
    body: str = json.loads(message.body.decode())
    print(body)

class ClientNotInitializedException(Exception):
    pass

class AsyncPikaClient:
    def __init__(
        self, 
        connection_string: str,
        queue_name: str,
    ):
        self.connection_string: str = connection_string
        self.queue_name: str = queue_name

        self.connection: Optional[Connection] = None
        self.channel: Optional[Channel] = None
        self.queue: Optional[Queue] = None
        self.consumer_callback: Optional[ConsumerFunction] = None

    @classmethod
    async def startup(
        cls,
        connection_string: str = RABBITMQ_CONNECTION_STRING, 
        queue_name: str = RABBITMQ_QUEUE_NAME,
        consumer_callback: AsyncFunction = boilderplate_consumer
    ):
        self = AsyncPikaClient(
            connection_string=connection_string,
            queue_name=queue_name
        )
        self.connection = await aio_pika.connect_robust(
            url=connection_string
        )
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(
            queue_name,
            durable=True
        )
        self.consumer_callback = consumer_callback

        return self

    async def shutdown(self) -> None:
        if (self.connection):
            await self.channel.close()
            await self.connection.close()

    async def send_message(self, msg: str) -> Dict[str,str]:
        if not (self.channel):
            raise ClientNotInitializedException('Channel not initialized')
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=msg.encode()
            ),
            routing_key=self.queue_name
        )
        return {'status':'success'}
    
    async def consume_messages(self) -> None:
        if not self.queue:
            raise ClientNotInitializedException('Queue not initialized')
        
        await self.queue.consume(self.consumer_callback, no_ack=False)