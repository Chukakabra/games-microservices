import pika
import time
import random


def process_message(ch, method, properties, body):
    text = body.decode()
    delay = random.randint(1, 5)
    print(f'RECEIVED: "{text}" | случайная задержка {delay} сек')
    time.sleep(delay)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f'DONE: "{text}"')


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672)
)
channel = connection.channel()

exchange_name = 'dyachkov_fanout_exchange'
channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='fanout',
    durable=False
)

queue_name = 'ikbo-64-23_dyachkov_fanout'
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

channel.queue_bind(
    exchange=exchange_name,
    queue=queue_name
)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=queue_name,
    auto_ack=False,
    on_message_callback=process_message
)

print('Waiting for messages...')
channel.start_consuming()