from django.core.mail import EmailMultiAlternatives
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from datetime import datetime
import logging
import os
import json

def send_mail(to,subject,body):
    msg = EmailMultiAlternatives(subject, to=[to])
    msg.attach_alternative(body, "text/html")
    msg.send()


def hosts(server_list, port):
    suffix = ':'+port+','
    return suffix.join(server_list)+suffix


class Consumer():

    def __init__(self, server_list, kafka_port, topic_name, consumer_name, email_address):
        self.server_list = server_list
        self.kafka_port = kafka_port
        self.topic_name = topic_name
        self.consumer_name = consumer_name
        self.email_address = email_address

    def listen(self):
        client = KafkaClient(hosts(self.server_list, self.kafka_port))
        client.ensure_topic_exists(self.topic_name)
        consumer = SimpleConsumer(client, self.consumer_name, self.topic_name)
        for message in consumer:
            value = message.message.value
            value = json.loads(value)
            if value['no'] % 10 == 0:
                print value
                subject = "test mail => "+message.message.value
                body = "Good day! Now is "+datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                send_mail(self.email_address,subject,body)



def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    server_list = ['10.251.21.176']
    kafka_port = '9092'
    topic_name = 'cnc_tool_1_temperature'
    consumer_name = 'sean.h.kim'
    email_address = consumer_name+"@samsung.com"
    consumer = Consumer(server_list, kafka_port, topic_name, consumer_name, email_address)
    consumer.listen()

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.ERROR
    )
    main()
