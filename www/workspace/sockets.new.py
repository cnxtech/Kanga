import logging
import threading
import json
import signal
import sys
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
                # print("Starting Kafka Client")
                # print("Kafka topic: {}").format(self.topic)
                print get_kafka_hosts()
                client = KafkaClient(hosts=get_kafka_hosts())
                consumer = SimpleConsumer(client=client, group=self.groupName.encode('ascii','ignore'), topic=self.topic,iter_timeout=5)
                consumer.seek(0, 1)
                print '[Kafka Consumer] START'
                print 'Topic: {}'.format(self.topic)
                print 'Listening incoming message...'
                print '========================================================='
                # print("Listening kafka message...")

                while self.stopCpu is False:
                    for message in consumer.get_messages(count=5, block=False):
                        if self.stopCpu is True:
                            # print("Kafka Consumer Listening Stopped")
                            break

                        if message:
                            offset = message.offset
                            value = message.message.value
                            print 'msg: {0}, offset: {1}'.format(value, offset)

                            if len(value) > 0:
                                # chartdata = []
                                # j_val = json.loads(value)
                                # j_val['offset'] = offset
                                # chartdata.append(j_val)
                                # print("destination => ws"+str(self.pid))
                                # self.parentOj.emit("ws"+str(self.type), chartdata)
                                # self.parentOj.emit(self.topic, value)
                                self.parentOj.emit("ws"+str(self.pid), value)

                print '[Kafka Consumer] STOP'
                print 'Topic: {}'.format(self.topic)
                print 'Stop listening...'
                print '========================================================'
                # print("Listening kafka Stopped")
                consumer.stop()
                client.close()
            except Exception as e:
                consumer.stop()
                client.close()

    def initialize(self):
        signal.signal(signal.SIGTERM, self.signal_term_handler)
        print '============== [SocketIO] OPEN NEW SESSION =============='
        print 'Session ID: [{}]'.format(self.socket.sessid)
        print 'User: {}'.format(self.request.user)
        print "============== SOCKET SESSIONS STARTED =============="
        self.logger = logging.getLogger("socketio.chat")
        self.log("Socketio session started")

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
        print '=============== [SocketIO] CLOSE SESSION ================'
        print 'Session ID: [{}]'.format(self.socket.sessid)
        print 'User: {}'.format(self.request.user)
        print "============== SOCKET DISCONNECTED =============="
        self.unregisterRequest()
        self.log('Disconnected')
        self.disconnect(silent=True)
        self.unregisterRequest()
        return True

    def unregisterRequest(self):
        # print("Removing existing Kafka handler with UID :"+self.socket.sessid)
        for cTh in threads:
            if cTh["key"] is self.socket.sessid:
                cTh["instance"].stopCpu = True
                threads.remove(cTh)

    def createNewKafkaHandler(self, topic, pid):
        timestamp = self.totimestamp(datetime.now())
        s = "_"
        seq = ("Consumer", str(self.request.user), str(timestamp))
        newGroupName = s.join(seq)
        # newGroupName = "Consumer_" + str(self.request.user)
        # print(">> Create New Kafka Handler with groupname : "+ newGroupName)
        th = self.KafkaConsumer(self)
        th.groupName = newGroupName
        th.topic = str(topic)
        th.pid = pid
        th.start()
        threads.append({"key": self.socket.sessid, "UID": newGroupName, "instance": th})

    def signal_term_handler(self,signal, frame):
        print 'got SIGTERM'
        self.unregisterRequest()
        #sys.exit(0)

    def on_user_message(self, msg):
        # print "============== MESSAGE RECEIVED =============="
        # self.log('User message: {0}'.format(msg))
        # print json.dumps(msg, sort_keys=True, indent=4)

        if msg.get("command"):
            if msg.get("command") == "stop":
                # print "Stopping...."
                self.unregisterRequest()
            elif msg.get("command") == "start":
                # print "Starting..."
                topic = msg.get("topic")
                pid = msg.get("pid")
                self.createNewKafkaHandler(topic, pid)
        #self.emit('cpu_data', {'point': 100})
        return True

    def totimestamp(self, dt, epoch=datetime(1970, 1, 1)):
        td = dt - epoch
        timestamp = (1e-6 * td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6
        return int(timestamp)