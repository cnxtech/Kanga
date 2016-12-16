import json
from datetime import datetime
import kazoo.client
KAZOO_CLIENT = kazoo.client.KazooClient
from knowledge.utils import utils


class KafkaZKHelper:

    def __init__(self):
        # TODO: How to handle multiple ZK servers?
        # TODO: Make ZK address configurable
        try:
            self.zk = KAZOO_CLIENT(hosts='10.251.23.21:2181')
            self.zk.start(timeout=10)
        except:
            print 'Error connecting to ZK node'
            self.zk = None


    def stop(self):
        if self.zk:
            self.zk.stop()


    def _get_children(self, zk_path):
        children_list = []
        try:
            children_list = self.zk.get_children(zk_path)
        except:
            return False, children_list

        return True, children_list


    def _get_data(self, zk_path):
        out_json = None
        try:
            data, stat = self.zk.get(zk_path)
        except:
            print 'Error fetching data from ZK path : ' + zk_path
            return False, out_json

        try:
            out_json = json.loads(data)
        except:
            print 'Error decoding json data from zk.get!'
            return False, out_json

        return True, out_json

    def get_broker_list(self):
        out_broker_list = []
        if self.zk is None:
            return 'ZK connection timeout', out_broker_list

        status, brokers = self._get_children('/brokers/ids')

        if status:
            for broker in brokers:
                status, broker_node = self._get_data('/brokers/ids/'
                                                     + broker)
                if status:
                    broker_node['broker_id'] = (str(broker))
                    broker_node['host'] = broker_node['host']
                    broker_node['alive_since'] = datetime \
                        .fromtimestamp(int(broker_node['timestamp']) / 1000) \
                        .strftime('%Y-%m-%d %H:%M:%S%z')

                    out_broker_list.append(broker_node)
                else:
                    continue

        else:
            return status, 'Error - finding list of Kafka brokers', out_broker_list

        return True, 'success', out_broker_list


    def get_topic(self, topic):
        out_topic_list = []
        if self.zk is None:
            return 'ZK connection timeout', out_topic_list

        status, partitions = self._get_children('/brokers/topics/'
                                                + topic
                                                + '/partitions')
        if status:
            for partition in partitions:
                status, partition_node = self._get_data('/brokers/topics/'
                                                        + topic
                                                        + '/partitions/'
                                                        + partition
                                                        + '/state')

                if status:
                    partition_node['topic'] = utils.add_anchor(topic)
                    partition_node['isr'] = ', '.join(str(isr) for isr in partition_node['isr'])
                    partition_node['partition'] = partition
                    out_topic_list.append(partition_node)
                else:
                    print 'Warning - No state info found under topic : ' + topic
                    continue
        else:
            print 'Error - No partitions found for topic : ' + topic
            return False, 'Error finding Kafka topic', out_topic_list


        return True, 'success', out_topic_list


    def get_topic_list(self):
        out_topic_list = []
        if self.zk is None:
            return 'ZK connection timeout', out_topic_list

        status, topics = self._get_children('/brokers/topics/')
        if status:
            for topic in topics:
                status, reason, topic_list = self.get_topic(topic)
                if status:
                    out_topic_list += topic_list
                else:
                    print 'Warning - Problem in fetching information about topic : ' + topic
                    continue

        else:
            return False, 'Error - finding list of Kafka topics', out_topic_list

        return True, 'success', out_topic_list


    def get_topic_offset_list(self):
        out_topic_offset_list = []
        if self.zk is None:
            return 'ZK connection timeout', out_topic_offset_list

        status, consumer_groups = self._get_children('/consumers')
        if status:
            for consumer_group in consumer_groups:
                status, topics = self._get_children('/consumers/'
                                                    + consumer_group
                                                    + '/offsets')
                if status:
                    for topic in topics:
                        status, partitions = self._get_children('/consumers/'
                                                                + consumer_group
                                                                + '/offsets/'
                                                                + topic)
                        if status:
                            for partition in partitions:
                                status, offset = self._get_data('/consumers/'
                                                                + consumer_group
                                                                + '/offsets/'
                                                                + topic
                                                                + '/'
                                                                + partition)

                                if status:
                                    partition_node = {'consumer_group': consumer_group,
                                                      'topic': utils.add_anchor(topic),
                                                      'partition': partition,
                                                      'offset': offset}
                                    out_topic_offset_list.append(partition_node)
                                else:
                                    print 'Warning - No offset found under partition : ' + partition
                                    continue
                        else:
                            print 'Warning - No partitions found under topic : ' + topic
                else:
                    print 'Warning - No topics found under consumer group : ' + consumer_group
                    continue
        else:
            return False, 'Error - finding list of Kafka consumer groups', out_topic_offset_list

        return True, 'success', out_topic_offset_list


    """
    TODO: Code duplication, Need to fix
    """
    def get_topic_summary(self, topic):
        topic_detail = {topic: []}
        if self.zk is None:
            return 'ZK connection timeout', topic_detail

        status, reason, broker_details = self.get_topic(topic)
        status, consumer_groups = self._get_children('/consumers')
        if status:
            for consumer_group in consumer_groups:
                status, topics = self._get_children('/consumers/'
                                                    + consumer_group
                                                    + '/offsets')
                if status:
                    for t in topics:
                        if topic == t:
                            cg_detail = {consumer_group: []}
                            status, partitions = self._get_children('/consumers/'
                                                                    + consumer_group
                                                                    + '/offsets/'
                                                                    + topic)

                            if status:
                                for partition in partitions:
                                    partition_detail = {partition: []}
                                    status, offset = self._get_data('/consumers/'
                                                                    + consumer_group
                                                                    + '/offsets/'
                                                                    + topic
                                                                    + '/'
                                                                    + partition)

                                    if status:
                                        detail = {'offset': offset}
                                        for broker_detail in broker_details:
                                            print broker_detail['partition']
                                            print partition
                                            if broker_detail['partition'] == partition:
                                                detail['leader'] = broker_detail['leader']
                                                detail['isr'] = broker_detail['isr']
                                        partition_detail[partition].append(detail)
                                        cg_detail[consumer_group].append(partition_detail)
                                    else:
                                        print 'Warning - No offset found under partition : ' + partition
                                        continue
                            else:
                                print 'Warning - No partitions found under topic : ' + topic
                            topic_detail[topic].append(cg_detail)
                else:
                    print 'Warning - No topics found under consumer group : ' + consumer_group
                    continue
        else:
            return False, 'Error - finding list of Kafka consumer groups', topic_detail

        return True, 'success', topic_detail