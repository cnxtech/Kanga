from kafka.client import KafkaClient
from kafka.producer import SimpleProducer
import time
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
        producer = SimpleProducer(client, batch_send=False)
        print producer
        no = 1
        for i in xrange(1,10000):
            with open(self.csvfile, 'r') as FR:
                first_line = next(FR)
                print first_line
                fields = first_line.lstrip().rstrip().split('\t')
                print fields
                for cnc_log in FR:
                    print cnc_log
                    values = cnc_log.strip().split('\t')
                    zipped = dict(zip(fields,values))
                    zipped['lower_bound'] = float(zipped['lower_bound'])
                    zipped['upper_bound'] = float(zipped['upper_bound'])
                    zipped['spindle'] = float(zipped['spindle'])
                    # zipped['no'] = int(zipped['no'])
                    zipped['no'] = no
                    zipped['tool_no'] = int(zipped['tool_no'])
                    # zipped['tool_no'] = i
                    print json.dumps(zipped,sort_keys=True,indent=4)
                    sleep_sec = 1
                    time.sleep(sleep_sec)
                    producer.send_messages(self.topic_name, json.dumps(zipped))
                    no = no +1


def main():
    file = 'spindle.tsv'
    csvfile = os.path.dirname(os.path.realpath(__file__))+"\\"+file
    print csvfile
    server_list = ['10.251.21.176']
    kafka_port = '9092'
    topic_name = 'cnc_tool_1_spindle'
    producer = Producer(csvfile, server_list, kafka_port, topic_name)
    producer.forwarder()

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.ERROR
    )
    main()
