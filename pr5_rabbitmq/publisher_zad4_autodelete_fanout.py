import pika
import sys

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

message = ' '.join(sys.argv[1:]) or 'Клиент уведомлён'
channel.basic_publish(
    exchange=exchange_name,
    routing_key='',
    body=message
)

print(f'SENT: "{message}"')
connection.close()