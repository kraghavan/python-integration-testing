import pika
import traceback

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = 'test'
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
BLOCKED_CONNECTION_TIMEOUT = 300

class RabbitMQPublisher:
    def __init__(self, host=RABBITMQ_HOST, port=RABBITMQ_PORT, queue=RABBITMQ_QUEUE):
        self.host = host
        self.port = port
        self.queue = queue
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            # Define RabbitMQ server credentials
            credentials=pika.PlainCredentials(username=RABBITMQ_USERNAME, 
                                            password=RABBITMQ_PASSWORD)
            # Define connection parameters
            parameters = pika.ConnectionParameters(credentials=credentials, 
                                                host=self.host, 
                                                port=self.port, 
                                                blocked_connection_timeout=BLOCKED_CONNECTION_TIMEOUT)

            # Establish connection
            self.connection = pika.BlockingConnection(parameters)

            # Create a new channel
            self.channel = self.connection.channel()

            # Declare a queue
            self.channel.queue_declare(queue=self.queue, durable=True)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

    def send_message(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)
        print(f" [x] Sent {message} to rabbitmq queue {self.queue}")

    def close(self):
        self.connection.close()

class RabbitMQConsumer:
    def __init__(self, host=RABBITMQ_HOST, queue=RABBITMQ_QUEUE, port=RABBITMQ_PORT, username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD, blocked_connection_timeout=BLOCKED_CONNECTION_TIMEOUT):
        self.host = host
        self.queue = queue
        self.password = password
        self.username = username
        self.connection = None
        self.channel = None

    def connect(self):
        credentials=pika.PlainCredentials(username=RABBITMQ_USERNAME, 
                                        password=RABBITMQ_PASSWORD)
        # Define connection parameters
        parameters = pika.ConnectionParameters(credentials=credentials, 
                                               host=self.host, 
                                               port=self.port, 
                                               blocked_connection_timeout=BLOCKED_CONNECTION_TIMEOUT)
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def callback(self, ch, method, properties, body):
        print("Received %r" % body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback)
        print('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
