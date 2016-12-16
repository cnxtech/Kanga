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

    def __init__(self, csvfile, server_list, kafka_port, topic_name):
        self.csvfile = csvfile
        self.server_list = server_list
        self.kafka_port = kafka_port
        self.topic_name = topic_name

    def forwarder(self):
        client = KafkaClient(hosts(self.server_list, self.kafka_port))
        client.ensure_topic_exists(self.topic_name)
        producer = SimpleProducer(client, batch_send=False)
        print producer
        for i in xrange(1,100):
            with open(self.csvfile, 'r') as FR:
                fields = next(FR).strip().split('\t')
                print fields
                for cnc_log in FR:
                    values = cnc_log.strip().split('\t')
                    zipped = dict(zip(fields,values))
                    zipped['lower_bound'] = float(zipped['lower_bound'])
                    zipped['upper_bound'] = float(zipped['upper_bound'])
                    zipped['temperature'] = float(zipped['temperature'])
                    zipped['no'] = int(zipped['no'])
                    print json.dumps(zipped,sort_keys=True,indent=4)
                    # prob = 0.8
                    # y = lambda x, prob: '<span style="background-color:#bd362f; color:white">FAIL</span>' if randint(0,x) > x*prob  else 'PASS'
                    # cnc_log = (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')+"\t"+y(10,0.8)+'\t'+cnc_log.strip()).split('\t')
                    # zipped = dict(zip(fields,cnc_log))
                    # node = zipped
                    sleep_sec = random.uniform(0,3)*5
                    time.sleep(sleep_sec)
                    producer.send_messages(self.topic_name, json.dumps(zipped))


def main():
    file = 'temperature.log'
    csvfile = os.path.dirname(os.path.realpath(__file__))+"\\"+file
    print csvfile
    # server_list = ['10.251.21.193', '10.251.21.176', '10.251.21.210']
    server_list = ['10.251.21.176']
    kafka_port = '9092'
    # topic_name = 'cnc_log_topic'+datetime.now().strftime('%Y%m%d_%H%M%S')
    topic_name = 'cnc_tool_1_temperature'
    producer = Producer(csvfile, server_list, kafka_port, topic_name)
    producer.forwarder()

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.ERROR
    )
    main()
