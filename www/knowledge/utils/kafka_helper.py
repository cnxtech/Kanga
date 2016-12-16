import traceback
from kafka import SimpleProducer, KafkaClient, KafkaConsumer
from knowledge import settings as kw_settings
import time


class KafkaHelper:
    """
    Utility class to interact with Kafka Brokers
    Internally uses kafka-python library
    """

    def __init__(self):
        # TODO: Make kafka broker list configurable
        try:
            self.kafka = KafkaClient(kw_settings.KW_KAFKA_BROKER_LIST)
        except:
            print 'Error - connecting to Kafka broker : ' + kw_settings.KW_KAFKA_BROKER_LIST
            self.kafka = None

        self.retry_count = 5
        self.retry_interval_in_ms = 5000


    def close(self):
        if self.kafka:
            self.kafka.close()


    def _ensure_kafka_topic_exists(self, topic):
        result = False
        for i in range(self.retry_count):
            try:
                self.kafka.ensure_topic_exists(topic)
                result = True
                break
            except:
                print 'Warning - Unable to create kafka topic : ' + topic
                print traceback.print_exc()
                time.sleep(self.retry_interval_in_ms / 1000)

        return result


    def upload_file_to_kafka(self, topic, file_path, **kwargs):
        """
        Utility function to upload contents of file to a given kafka topic
        :param topic: Kafka topic to which the file will be uploaded
        :param file_path: Absolute path of the file to be uploaded
        :param kwargs: append - If True, then file content will be uploaded to existing topic. If topic is not present
        then new one will be created.
        If false, and topic is not present then new topic is created. If topic is already present then error is returned.
        Default, async=False
        :return: True if content was uploaded else false
        """
        append = kwargs.get('append', False)
        result = False
        producer = None
        try:
            if not append:
                # Check if topic is already present
                if self.kafka.has_metadata_for_topic(topic):
                    print 'Error - Kafka topic : ' + topic + ' already present and append is : ' + str(append)
                    return False

            # In case of append is True and topic already present/not present
            # and append is False and topic already not present
            if self._ensure_kafka_topic_exists(topic):
                producer = SimpleProducer(self.kafka, batch_send=True,
                                          batch_send_every_n=20)
                with open(file_path, 'rU') as fh:
                    for line in fh:
                        producer.send_messages(topic, line.strip())
                result = True

        except:
            print 'Error - uploading file : ' + file_path + ' to topic : ' + topic
        finally:
            if producer:
                producer.stop()
        return result
