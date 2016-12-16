from kafka.client import KafkaClient
from kafka.producer import SimpleProducer
from datetime import datetime
from random import randint
import time
import random
import logging
import os
import json
import pprint


def hosts(server_list, port):
    suffix = ':'+port+','
    return suffix.join(server_list)+suffix


class Producer():

    def __init__(self, server_list, kafka_port, topic_name):
        self.server_list = server_list
        self.kafka_port = kafka_port
        self.topic_name = topic_name
        self.client = KafkaClient(hosts(self.server_list, self.kafka_port))
        self.producer = SimpleProducer(self.client, batch_send=False)

    def ensure_topic_exists(self):
        self.client.ensure_topic_exists(self.topic_name)

    def forwarder(self,message):
        self.producer.send_messages(self.topic_name, message)


def main():
    server_list = ['10.251.21.176']
    kafka_port = '9092'
    topic_name = 'cnc_tool_2_temperature'
    producer = Producer(server_list, kafka_port, topic_name)
    producer.ensure_topic_exists()
    ref_temp = 8.46
    drift_ratio = 20
    epsilo_ratio = 15

    for i in xrange(1,100000):
        drift = random.uniform(-10,10)/drift_ratio
        epsilon  = random.uniform(-10,10)/epsilo_ratio
        ref_temp += drift
        temp = ref_temp + epsilon
        msg = {
            "no": i,
            "temperature": temp,
            "ref_temperature": ref_temp
        }
        print json.dumps(msg,sort_keys=True,indent=4)
        producer.forwarder(json.dumps(msg))
        sleep_sec = random.uniform(0,3)
        time.sleep(sleep_sec)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.ERROR
    )
    main()
