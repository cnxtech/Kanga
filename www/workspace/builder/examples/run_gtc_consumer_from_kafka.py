from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from datetime import datetime
import logging


def hosts(server_list, port):
    suffix = ':'+port+','
    return suffix.join(server_list)+suffix


class Consumer():

    def __init__(self, server_list, kafka_port, topic_name, consumer_name):
        self.server_list = server_list
        self.kafka_port = kafka_port
        self.topic_name = topic_name
        self.consumer_name = consumer_name

    def listen(self):
        client = KafkaClient(hosts(self.server_list, self.kafka_port))
        client.ensure_topic_exists(self.topic_name)
        # print client.topic_partitions()
        consumer = SimpleConsumer(client, self.consumer_name, self.topic_name)
        for message in consumer:
            value = message.message.value
            print value


def main():
    server_list = ['kanga']
    kafka_port = '9092'
    topic_name = 'cnc_log_topic'+datetime.now().strftime('%Y%m%d')
    consumer_name = 'cnc_log_consumer'+datetime.now().strftime('%Y%m%d%H%M%S')
    consumer = Consumer(server_list, kafka_port, topic_name, consumer_name)
    consumer.listen()

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.ERROR
    )
    main()