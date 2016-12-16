from kafka.client import KafkaClient
from kafka.producer import SimpleProducer
from datetime import datetime
from random import randint
import time
import random
import logging
import os
import json


def hosts(server_list, port):
    suffix = ':'+port+','
    return suffix.join(server_list)+suffix


class Producer():

    def __init__(self, csvfile, server_list, kafka_port, topic_name):
        self.csvfile = csvfile
        self.server_list = server_list
        self.kafka_port = kafka_port
        self.topic_name = topic_name

    def forwarder(self):
        client = KafkaClient(hosts(self.server_list, self.kafka_port))
        client.ensure_topic_exists(self.topic_name)
        # print client.topic_partitions()
        producer = SimpleProducer(client, batch_send=False)
        for i in xrange(1,100):
            with open(self.csvfile, 'r') as FR:
                fields = ("ARRIVAL_TIMESTAMP\t"+"DEFECT\t"+next(FR).strip()).split('\t')
                for cnc_log in FR:
                    prob = 0.8
                    y = lambda x, prob: '<span style="background-color:#bd362f; color:white">FAIL</span>' if randint(0,x) > x*prob  else 'PASS'
                    cnc_log = (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')+"\t"+y(10,0.8)+'\t'+cnc_log.strip()).split('\t')
                    zipped = dict(zip(fields,cnc_log))
                    node = zipped
                    sleep_sec = random.uniform(0,10)
                    time.sleep(sleep_sec)
                    producer.send_messages(self.topic_name, json.dumps(node))


def main():
    file = 'days5_all_cnc7_notmissing_500grand.log'
    # file = 'days5_all_cnc7_notmissing_500grand_selected.log'
    csvfile = os.path.dirname(os.path.realpath(__file__))+"\\"+file
    print csvfile
    # server_list = ['10.251.21.193', '10.251.21.176', '10.251.21.210']
    server_list = ['10.251.21.176']
    kafka_port = '9092'
    # topic_name = 'cnc_log_topic'+datetime.now().strftime('%Y%m%d_%H%M%S')
    topic_name = 'cnc_log_topic'
    producer = Producer(csvfile, server_list, kafka_port, topic_name)
    producer.forwarder()

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.ERROR
    )
    main()