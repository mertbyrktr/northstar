import asyncio
import os
import json
import aio_pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

async def test_pipeline():
    print(f"Connecting to RabbitMQ at {RABBITMQ_URL}...")
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_URL)
    except Exception as e:
        print(f"Failed to connect: {e}")
        return False
        
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("test_queue", durable=True)
        
        payload = {"message": "Hello Northstar RabbitMQ Test!"}
        print("Publishing test message...")
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(payload).encode("utf-8"),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key="test_queue"
        )
        print("Message published successfully.")
        
        print("Waiting for message to consume...")
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body.decode("utf-8"))
                    print(f"Successfully consumed test message: {data}")
                    assert data["message"] == payload["message"]
                    break
                    
    print("Test passed successfully!")
    return True

if __name__ == "__main__":
    asyncio.run(test_pipeline())
