from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

import subprocess

KAFKA_CONTAINER_NAME = "my_kafka_container"
KAFKA_HOST = "kafka"
KAFKA_PORT = 9092
KAFKA_TOPIC = 'test'

class KafkaProducer:
    def __init__(self, host=KAFKA_HOST, port=KAFKA_PORT, topic=KAFKA_TOPIC):
        self.host = host
        self.port = port
        self.topic = topic
        self.producer = Producer({
            'bootstrap.servers': f"{self.host}:{self.port}"
        })

    def list_kafka_topics(self):
        admin_client = AdminClient({'bootstrap.servers': f"{KAFKA_HOST}:{KAFKA_PORT}"})
        cluster_metadata = admin_client.list_topics(timeout=10)
        return [topic.topic for topic in cluster_metadata.topics.values()]

    def create_kafka_topic_if_not_exists(self, topic_name):
        # List all topics
        list_topics = self.list_kafka_topics()

        # Check if the topic exists
        if topic_name in list_topics:
            print(f"Topic '{topic_name}' already exists.")
        else:
            # Create the topic
            admin_client = AdminClient({'bootstrap.servers': f"{self.host}:{self.port}"})
            topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
            admin_client.create_topics([topic])
            print(f"Topic '{topic_name}' created.")

    def delivery_report(self, err, message):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {message.topic()} [{message.partition()}]")

    def produce_message(self, message):
        try:
        # Check if the topic exists and create it if it doesn't
            self.create_kafka_topic_if_not_exists(topic_name=KAFKA_TOPIC)

            # Send the message to the 'my_topic' topic
            self.producer.produce(topic=KAFKA_TOPIC, value=message, callback=self.delivery_report)
            
            self.producer.poll(0)
        except Exception as e:
            print(f"An error occurred: {e}")

    def close(self):
        self.producer.flush()


