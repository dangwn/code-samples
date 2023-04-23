from fastapi import (
    FastAPI,
    Response, 
    status
)
import uvicorn

from AsyncPikaClient import AsyncPikaClient
from config import (
    PRODUCER_API_HOST,
    PRODUCER_API_PORT
)

app = FastAPI()

@app.on_event('startup')
async def app_startup():
    app.rabbitmq_client: AsyncPikaClient = await AsyncPikaClient.startup()

@app.on_event('shutdown')
async def app_shutdown():
    await app.rabbitmq_client.shutdown()

@app.post('/', status_code=status.HTTP_202_ACCEPTED)
async def send_message(
    msg: str
) -> Response:
    await app.rabbitmq_client.send_message(msg)

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=PRODUCER_API_HOST,
        port=PRODUCER_API_PORT
    )