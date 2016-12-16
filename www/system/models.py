from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Cluster(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name


class Node(models.Model):
    cluster = models.ForeignKey(Cluster)
    ip = models.CharField(max_length=20, blank=False, null=False, primary_key=True)
    hostname = models.CharField(max_length=40)
    def __unicode__(self):
        return self.ip


class Service(models.Model):
    KAFKA = 'KAFKA'
    STORM = 'STORM'
    ELASTICSEARCH = 'ELASTICSEARCH'
    ZOOKEEPER = 'ZOOKEEPER'
    DJANGO = 'DJANGO'
    POSTGRESQL = 'POSTGRESQL'
    SQLITE = 'SQLITE'
    OS = 'OS'
    BACKEND_CHOICES = (
        (KAFKA, 'Kafka'),
        (STORM, 'Storm'),
        (ELASTICSEARCH, 'ElasticSearch'),
        (ZOOKEEPER, 'Zookeeper'),
        (DJANGO, 'Django'),
        (POSTGRESQL, 'PostgreSql'),
        (SQLITE, 'Sqlite'),
        (OS, 'OperatingSystem'),
    )
    BUSY = 'BUSY'
    GOOD = 'GOOD'
    WARNING = 'WARN'
    ERROR = 'ERR'
    ACTIVE_CHOICES = (
        (BUSY, 'Busy'),
        (GOOD, 'Good'),
        (WARNING, 'Warning'),
        (ERROR, 'Error'),
    )
    SERVICE = 'SERVICE'
    MONITORING = 'MONITORING'
    PURPOSE_CHOICES = (
        (SERVICE, 'Service_port'),
        (MONITORING, 'Monitoring_port'),
    )
    node = models.ForeignKey(Node)
    name = models.CharField(max_length=30, primary_key=True)
    port = models.IntegerField()
    code = models.CharField(max_length=15, choices=BACKEND_CHOICES)
    active = models.CharField(max_length=4, choices=ACTIVE_CHOICES)
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return str(self.name)+","+str(self.node.ip)+':'+str(self.port)


class DatabaseService(models.Model):
    service = models.ForeignKey(Service)
    connection_name = models.CharField(max_length=30, primary_key=True)
    db_name = models.CharField(max_length=150) # if db is sqlite, it is full path file name. if oracle, tns name. if ms sql over odbc, odbc dsn
    user = models.CharField(max_length=30, default='', blank=True)
    password = models.CharField(max_length=30, default='', blank=True)
    def __unicode__(self):
        return str(self.connection_name)+" @"+str(self.service)


class Config(models.Model):
    service = models.ForeignKey(Service)
    filename = models.CharField(max_length=100, default='',unique=True)
    content = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return str(self.service)+" > "+str(self.filename)


class JobScript(models.Model):
    # An id field is added automatically as primary key (auto increment)
    name = models.CharField(max_length=50, default='')
    description = models.TextField(default='')
    script = models.TextField(default='')
    user_id = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name

class ConnectedDevice(models.Model):
    ARTIK5 = 'ARTIK5'
    ARTIK7 = 'ARTIK7'
    ARTIK10 = 'ARTIK10'
    RASPBERRYPI2 = 'Raspberry Pi2'
    RASPBERRYPI3 = 'Raspberry Pi3'
    ODROID_XU4 = 'ODROID-XU4'
    LINUX = 'Linux-PC'
    WINDOWS = 'Windows-PC'
    type_chioces = (
        (ARTIK5, 'Artik5'),
        (ARTIK7, 'Artik7'),
        (ARTIK10, 'Artik10'),
        (RASPBERRYPI2, 'Raspberry Pi2'),
        (RASPBERRYPI3, 'Raspberry Pi3'),
        (ODROID_XU4, 'Odroid-xu4'),
        (LINUX, 'Linux-pc'),
        (WINDOWS, 'Windows-pc')
    )
    deviceType = models.CharField(max_length=50, choices=type_chioces)
    ip = models.CharField(max_length=20, blank=False, null=False, primary_key=True)
    hostname = models.CharField(max_length=50, default='', null=True)
    description = models.TextField(default='', null=True)
    def __unicode__(self):
        return self.ip
