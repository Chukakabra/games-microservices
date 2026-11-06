import pika
import time

def process_message(ch, method, properties, body):
    text = body.decode()
    delay = text.count('.')
    print(f'RECEIVED: "{text}" | точек: {delay} → задержка {delay} сек')
    time.sleep(delay)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f'DONE: "{text}"')


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672)
)
channel = connection.channel()

exchange_name = 'zamorskiy_topic_exchange'
channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='topic',
    durable=False
)

queue_name = 'ikbo-64-23_zamorskiy_auto'
channel.queue_declare(
    queue=queue_name,
    durable=False,
    exclusive=True,
    auto_delete=True,
    arguments={
        'x-expires': 60000,
        'x-message-ttl': 30000
    }
)

routing_key = 'order.*.created'
channel.queue_bind(
    exchange=exchange_name,
    queue=queue_name,
    routing_key=routing_key
)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=queue_name,
    auto_ack=False,
    on_message_callback=process_message
)

print('Waiting for messages...')
channel.start_consuming()