import pika
import sys

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

message = ' '.join(sys.argv[1:]) or 'Заказ..создан.'
channel.basic_publish(
    exchange=exchange_name,
    routing_key='order.game.created',
    body=message
)

print(f'SENT: "{message}" | точек: {message.count(".")}')
connection.close()