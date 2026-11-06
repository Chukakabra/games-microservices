import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672)
)
channel = connection.channel()

channel.queue_declare(
    queue="ikbo-64-23_timofeev_excl",
    exclusive=True,
    durable=False
)

def process_message(ch, method, properties, body):
    print(f'RECEIVED: {body.decode()}')

channel.basic_consume(
    queue="ikbo-64-23_timofeev_excl",
    auto_ack=True,
    on_message_callback=process_message
)

print('Waiting for messages...')
channel.start_consuming()
