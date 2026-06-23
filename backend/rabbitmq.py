import os
import json
import asyncio
import aio_pika
from aio_pika.pool import Pool

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
if not RABBITMQ_URL:
    print("WARNING: RABBITMQ_URL environment variable is empty or not set. Defaulting to local RabbitMQ: amqp://guest:guest@localhost:5672/")
    RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

connection_pool = None
channel_pool = None

async def get_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)

async def get_channel() -> aio_pika.Channel:
    async with connection_pool.acquire() as connection:
        return await connection.channel()

async def connect_rabbitmq():
    global connection_pool, channel_pool
    try:
        connection_pool = Pool(get_connection, max_size=2)
        channel_pool = Pool(get_channel, max_size=10)
        
        # Warmup: try to acquire one connection to ensure RabbitMQ is accessible
        async with connection_pool.acquire() as conn:
            pass
        print("Connected to RabbitMQ! Pools initialized successfully.")
    except Exception as e:
        print(f"Error initializing RabbitMQ connection pool: {e}")

async def close_rabbitmq():
    global connection_pool, channel_pool
    if channel_pool:
        try:
            await channel_pool.close()
        except Exception as e:
            print(f"Error closing RabbitMQ channel pool: {e}")
        print("Closed RabbitMQ channel pool.")
        channel_pool = None
        
    if connection_pool:
        try:
            await connection_pool.close()
        except Exception as e:
            print(f"Error closing RabbitMQ connection pool: {e}")
        print("Closed RabbitMQ connection pool.")
        connection_pool = None

async def publish_message(queue_name: str, message: dict):
    """
    Publishes a JSON-serializable message to the specified queue.
    Declares the queue as durable first.
    """
    global channel_pool
    if not channel_pool:
        print("RabbitMQ channel pool is not initialized. Cannot publish message.")
        return
        
    try:
        async with channel_pool.acquire() as channel:
            # Declare the queue (guarantees it exists and is durable)
            await channel.declare_queue(queue_name, durable=True)
            
            # Prepare message payload
            body = json.dumps(message).encode("utf-8")
            
            # Publish using the default exchange (routing key = queue_name)
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=body,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=queue_name
            )
            print(f"Successfully published message to queue '{queue_name}'")
    except Exception as e:
        print(f"Failed to publish message to queue '{queue_name}': {e}")
