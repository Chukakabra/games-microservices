import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672)
)
channel = connection.channel()

exchange_name = 'novachuk_direct_exchange'
channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='direct',
    durable=True
)

queue_name = 'ikbo-64-23_novachuk_durable'
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

message = ' '.join(sys.argv[1:]) or 'Заказ оформлен и оплачен'

channel.basic_publish(
    exchange=exchange_name,
    routing_key=routing_key,
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    )
)

print(f'SENT: "{message}" | длина: {len(message)} → задержка {len(message)} сек')
connection.close()