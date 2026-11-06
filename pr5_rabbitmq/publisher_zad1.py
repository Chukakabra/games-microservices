import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672)
)
channel = connection.channel()

message = "Тест эксклюзивной очереди"
channel.basic_publish(
    exchange='',
    routing_key="ikbo-64-23_timofeev_excl",
    body=message
)

print(f"SENT: {message}")
connection.close()
