from django.db import models
from django.contrib.auth.models import Group, User
from datetime import datetime



class RealtimeQuery(models.Model):
    # An id field is added automatically as primary key (auto increment)
    name = models.CharField(max_length=100, default='')
    query = models.TextField(default='')
    description = models.TextField(default='')
    user_id = models.ForeignKey(User)
    # created = models.DateTimeField(auto_now_add=True, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # updated = models.DateTimeField(auto_now=True, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    running = models.BooleanField(default=False)
    local_mode = models.BooleanField(default=False)
    query_option = models.TextField(default='')
    last_running = models.CharField(max_length=50, default='')
    jar_path = models.CharField(max_length=250, default='')
    def __unicode__(self):
        return self.name


class RealtimeQueryPermission(models.Model):
    # An id field is added automatically as primary key (auto increment)
    query = models.ForeignKey(RealtimeQuery)
    group = models.ForeignKey(Group)
    readable = models.BooleanField(default=False)
    writable = models.BooleanField(default=False)
    def __unicode__(self):
        return self.query.name+","+self.group.name


class BatchQuery(models.Model):
    # An id field is added automatically as primary key (auto increment)
    name = models.CharField(max_length=100,default='')
    query = models.TextField(default='')
    description = models.TextField(default='')
    user_id = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=False)
    scheduled_time = models.CharField(max_length=50,default='')
    scheduled = models.BooleanField(default=False)
    cron_schedule = models.CharField(max_length=100, default='')
    def __unicode__(self):
        return self.name


class BatchQueryPermission(models.Model):
    # An id field is added automatically as primary key (auto increment)
    query = models.ForeignKey(BatchQuery)
    group = models.ForeignKey(Group)
    readable = models.BooleanField(default=False)
    writable = models.BooleanField(default=False)
    def __unicode__(self):
        return str(self.query)+","+str(self.group)


class QueryLog(models.Model):
    # An id field is added automatically as primary key (auto increment)
    query = models.ForeignKey(BatchQuery)
    log = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.query+" @"+self.created