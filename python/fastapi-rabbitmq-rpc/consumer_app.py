import asyncio
from fastapi import (
    FastAPI,
    Response, 
    status
)
import uvicorn

from AsyncPikaClient import AsyncPikaClient
from config import (
    CONSUMER_API_HOST,
    CONSUMER_API_PORT,
    CONSUMER_MANUAL_CONSUME
)

from asyncio import AbstractEventLoop, Task

app: FastAPI = FastAPI()

@app.on_event('startup')
async def app_startup():
    app.rabbitmq_client: AsyncPikaClient = await AsyncPikaClient.startup()

    if not CONSUMER_MANUAL_CONSUME:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        task: Task = loop.create_task(app.rabbitmq_client.consume_messages())
        await task

@app.on_event('shutdown')
async def app_shutdown():
    await app.rabbitmq_client.shutdown()

if CONSUMER_MANUAL_CONSUME:
    @app.get('/', status_code=status.HTTP_204_NO_CONTENT)
    async def get_messages() -> Response:
        await app.rabbitmq_client.consume_messages()

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=CONSUMER_API_HOST,
        port=CONSUMER_API_PORT
    )