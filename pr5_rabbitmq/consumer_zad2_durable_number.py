import pika
import time

def process_message(ch, method, properties, body):
    text = body.decode()
    delay = len(text)
    print(f'RECEIVED: "{text}"')
    print(f'Длина = {delay} символов → симуляция нагрузки {delay} сек...')
    time.sleep(delay)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f'DONE: "{text}"')


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672)
)
channel = connection.channel()

exchange_name = 'timofeev_direct_exchange'
channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='direct',
    durable=True
)

queue_name = 'ikbo-64-23_timofeev_durable_number'
channel.queue_declare(
    queue=queue_name,
    durable=True,
    exclusive=False,
    auto_delete=False
)

routing_key = 'game_orders'
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