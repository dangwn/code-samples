## FastAPI Producer/Consumer with RabbitMQ
A boilerplate example for using two FastAPI apps connected via RabbitMQ, with one as a producer and one as a consumer, using AIO Pika.

The producer app has one endpoint, where a post request can be sent to put a message on to the queue. This is consumed by the consumer app in one of two ways:
```
if config.CONSUMER_MANUAL_CONSUME == True:
    Consumer consumes all messages in the queue when a get request is sent to the '/' endpoint
if config.CONSUMER_MANUAL_CONSUMER == False:
    Consumer polls queue for new messages and consumes immediately
```
A boilerplate consume callback is supplied which simply prints the message. Both the producer and consumer keep their connections with RabbitMQ open, until app shutdown.

To run RabbitMQ locally with docker, follow these instructions:
```
docker pull rabbitmq:3-management
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 5673:5673 -p 15672:15672 rabbitmq:3-management
```

Resources:
- [RabbitMQ in Python](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)
- [AIO Pika](https://aio-pika.readthedocs.io/en/latest/)
- [RabbitMQ publisher and consumer with FastAPI](https://itracer.medium.com/rabbitmq-publisher-and-consumer-with-fastapi-175fe87aefe1)
- [How to use FastAPI as consumer for RabbitMQ (RPC)](https://stackoverflow.com/questions/65586853/how-to-use-fastapi-as-consumer-for-rabbitmq-rpc)