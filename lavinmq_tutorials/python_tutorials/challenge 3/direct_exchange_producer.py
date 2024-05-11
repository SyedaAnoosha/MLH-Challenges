
# producer.py

import pika, os
from dotenv import load_dotenv

load_dotenv()

# Access the CLOUDAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')

# Create a connection
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
print("[✅] Connection over channel established")

channel = connection.channel() # start a channel

exchange_name = "slack_notifications_fanout"
channel.exchange_declare(
  exchange=exchange_name,
  exchange_type='direct'
) # Declare an exchange


queues = {
  "hr": "hr_queue", 
  "support": "support_queue", 
  "marketing": "marketing_queue"
} # binding_key: queue_name

# Declare three queues for each user groups
for _, queue_name in queues.items():
    channel.queue_declare(
        queue=queue_name,
        durable=True
    )


# Create bindings between the exchange and queues
for binding_key, queue_name in queues.items():
    channel.queue_bind(
        exchange=exchange_name,
        queue=queue_name,
        routing_key=binding_key
    )

def send_to_queue(channel, routing_key, body):
  channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=body,
        properties=pika.BasicProperties(
            delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
        )
  )
  print(f"[📥] Message sent to queue #{body}")

# Publish messages - one message for each user group
send_to_queue(
    channel=channel, routing_key="hr", body="New message in HR"
)
send_to_queue(
    channel=channel, routing_key="support", body="New message in Support"
)
send_to_queue(
    channel=channel, routing_key="marketing", body="New message in Marketing "
)

try:
  connection.close()
  print("[❎] Connection closed")
except Exception as e:
  print(f"Error: #{e}")
  