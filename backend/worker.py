import os
import sys
import json
import asyncio
import aio_pika

# Make sure we can import from the backend directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import connect_to_mongo, close_mongo_connection, get_db

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
if not RABBITMQ_URL:
    RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

async def handle_welcome_email(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body.decode("utf-8"))
            user_id = data.get("user_id")
            email = data.get("email")
            name = data.get("name")
            
            print(f"\n[WORKER] [WELCOME_EMAIL] Received registration event for user {user_id}")
            print(f"[WORKER] [WELCOME_EMAIL] Mock Sending email to: {email}")
            print(f"=========================================")
            print(f"Subject: Welcome to Northstar, {name}!")
            print(f"Body: Hello {name}, thank you for registering with Northstar Gym Tracker.")
            print(f"Start logging your workouts today and reach your goals!")
            print(f"=========================================\n")
        except Exception as e:
            print(f"[WORKER] [WELCOME_EMAIL] Error processing message: {e}")

async def handle_workout_summary(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body.decode("utf-8"))
            user_id = data.get("user_id")
            workout_id = data.get("workout_id")
            
            print(f"\n[WORKER] [WORKOUT_SUMMARY] Received summary generation request for user {user_id}, workout {workout_id}")
            print(f"[WORKER] [WORKOUT_SUMMARY] Simulating computation / AI summary generation...")
            
            # Simulate a time-consuming operation (e.g. AI API call or data analysis)
            await asyncio.sleep(2)
            
            print(f"[WORKER] [WORKOUT_SUMMARY] AI Summary Generation Completed for user {user_id}!")
            print(f"Workout {workout_id} analysis: Volume: 2400kg, Intensity: High, Focus: Hypertrophy.\n")
        except Exception as e:
            print(f"[WORKER] [WORKOUT_SUMMARY] Error processing message: {e}")

async def main():
    # Wait for databases to initialize
    await connect_to_mongo()
    
    print("[WORKER] Connecting to RabbitMQ...")
    # Re-connect logic loop in case RabbitMQ isn't ready immediately
    connection = None
    for attempt in range(10):
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            break
        except Exception as e:
            print(f"[WORKER] RabbitMQ connection attempt {attempt+1}/10 failed: {e}. Retrying in 3s...")
            await asyncio.sleep(3)
            
    if not connection:
        print("[WORKER] Failed to connect to RabbitMQ after 10 attempts. Exiting.")
        return

    print("[WORKER] Connected to RabbitMQ successfully. Registering consumers...")
    
    async with connection:
        channel = await connection.channel()
        
        # Prefetch value determines how many messages can be sent to worker before acknowledgment
        await channel.set_qos(prefetch_count=1)
        
        # Declare queues
        welcome_queue = await channel.declare_queue("welcome_emails", durable=True)
        summary_queue = await channel.declare_queue("workout_summaries", durable=True)
        
        # Start consuming
        await welcome_queue.consume(handle_welcome_email)
        await summary_queue.consume(handle_workout_summary)
        
        print("[WORKER] Listening for tasks on 'welcome_emails' and 'workout_summaries' queues. Press Ctrl+C to exit.")
        
        # Keep running
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            pass
        finally:
            await close_mongo_connection()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[WORKER] Interrupted by user. Exiting.")
