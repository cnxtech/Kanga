import logging
import threading
import json
import signal
import sys
import traceback
from django.conf import settings
from datetime import datetime, timedelta

from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace
from threading import Thread
from django.contrib.auth.models import User
from system.models import Service
from workspace.views_report import get_all_host
from data.views_kafka import get_kafka_hosts
from data.views_es import get_es_hosts

from elasticsearch import Elasticsearch

print "Socket Workspace Called****************"

exitapp = False

threads = []

@namespace('/workspace')
class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    nicknames = []

    class KafkaConsumer(Thread):
        stopCpu = False
        parentOj = None
        groupName = "public_group"
        topic = "tes"
        pid = ""

        def __init__(self, parentObj):
            threading.Thread.__init__(self)
            self.parentOj = parentObj

        def run(self):
            client = None
            consumer = None
            try:
                prev = None
                print("Starting Kafka Client")
                print("Kafka topic: {}").format(self.topic)

                hosts = get_es_hosts()
                print "es hosts: ", hosts
                es = Elasticsearch(hosts=hosts)
                # ES_HOST = {"host": "localhost", "port": 9200}
                # es = Elasticsearch(hosts=[ES_HOST])

                # host_list = get_all_host('KAFKA')
                hosts = get_kafka_hosts()
                print "kafka hosts: ", hosts
                client = KafkaClient(hosts=hosts)
                # print "kafka client group name: "+self.groupName
                consumer = SimpleConsumer(client, self.groupName, self.topic)
                # consumer.seek --> offset=0, whence=current
                consumer.seek(-5, 2)
                print("Listening kafka message...")

                while self.stopCpu is False:
                    # for message in consumer.get_messages(count=5, block=False):
                    for message in consumer:
                        if self.stopCpu is True:
                            print("Kafka Consumer Listening Stopped")
                            break

                        if message:
                            print "Consuming kafka message: ", message
                            value = message.message.value
                            try:
                                json_value = json.loads(value)
                                offset = message.offset
                                json_value['data'][0]['offset'] = offset
                                value = json.dumps(json_value)
                                print "Publishing data: ", value

                                doc = json.dumps(json_value['data'][0])
                                if len(doc) > 0:
                                    es.index(index='kafka', doc_type=self.topic, id=offset, body=doc)

                                if len(value) > 0:
                                    self.parentOj.emit("ws"+str(self.pid), value)
                            except Exception as e:
                                traceback.print_exc()
                                print "Skipping invalid message"
            except Exception as e:
                traceback.print_exc()
            finally:
                print("Listening kafka Stopped")
                print "Stopping consumer ..."
                consumer.stop()
                print "Closing client ..."
                client.close()



    def initialize(self):
        print "============== SOCKET SESSIONS STARTED =============="
        self.logger = logging.getLogger("socketio.chat")
        self.log("Socketio session started")
        signal.signal(signal.SIGTERM, self.signal_term_handler)

    def log(self, message):
        print "============== LOG =============="
        print self.request.user
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def on_join(self, room):
        print "============== JOIN =============="
        return True

    def on_nickname(self, nickname):
        print "============== NICKNAME =============="
        self.log('Nickname: {0}'.format(nickname))
        return True, nickname

    def recv_disconnect(self):
        print "============== SOCKET DISCONNECTED =============="
        self.unregisterRequest()
        self.log('Disconnected')
        self.disconnect(silent=True)
        unregisterRequest()
        return True

    def unregisterRequest(self):
        print("Removing existing Kafka handler with UID :"+self.socket.sessid)
        for cTh in threads:
            if cTh["key"] is self.socket.sessid:
                cTh["instance"].stopCpu = True
                threads.remove(cTh)

    def createNewKafkaHandler(self, topic, pid):
        # newGroupName = "Consumer_" + str(self.request.user) // OLD
        timestamp = self.totimestamp(datetime.now())
        s = "_"
        seq = ("KangaWeb","Consumer", str(self.request.user), str(timestamp))
        newGroupName = s.join(seq)
        print(">> Create New Kafka Handler with groupname : "+ newGroupName)
        th = self.KafkaConsumer(self)
        th.groupName = newGroupName
        th.topic = str(topic)
        th.pid = pid
        th.start()
        threads.append( {"key": self.socket.sessid, "UID":newGroupName, "instance": th} )

    def signal_term_handler(signal, frame):
        print 'got SIGTERM'
        unregisterRequest()
        #sys.exit(0)

    def on_user_message(self, msg):
        print "============== MESSAGE RECEIVED =============="
        self.log('User message: {0}'.format(msg))

        print json.dumps(msg, sort_keys=True, indent=4)

        if msg.get("command"):
            if msg.get("command") == "stop":
                print "Stopping...."
                self.unregisterRequest()
            elif msg.get("command") == "start":
                print "Starting..."
                topic = msg.get("topic")
                pid = msg.get("pid")
                self.createNewKafkaHandler(topic, pid)
        #self.emit('cpu_data', {'point': 100})
        return True

    def totimestamp(self, dt, epoch=datetime(1970, 1, 1)):
        td = dt - epoch
        timestamp = (1e-6 * td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6
        return int(timestamp)