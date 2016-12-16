from django.db import models
from knowledge.models import RealtimeQuery, BatchQuery
from django.contrib.auth.models import User
from datetime import datetime


class StreamingJobHistory(models.Model):
    LAUNCHED = 'LAUNCHED'
    FAILED = 'FAILED'
    KILLED = 'KILLED'
    ACTIVATED = 'ACTIVATED'
    DEACTIVATED = 'DEACTIVATED'
    REBALANCED = 'REBALANCED'
    STATES = (
        (LAUNCHED, 'Launched'),
        (FAILED, 'Failed'),
        (KILLED, 'Killed'),
        (ACTIVATED, 'Activated'),
        (DEACTIVATED, 'Deactivated'),
        (REBALANCED, 'Rebalanced'),
    )
    query = models.ForeignKey(RealtimeQuery, default='', null=True)
    user = models.ForeignKey(User)
    message = models.TextField(default='', null=True)
    state = models.CharField(max_length=10, choices=STATES)
    acked = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.query)+" @"+str(self.launched)

class StreamingJobHistoryDetail(models.Model):
    job_history = models.ForeignKey(StreamingJobHistory)
    message = models.TextField(default='', null=True)
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.job_history)+" @"+str(self.created)

class BatchJobHistory(models.Model):
    LAUNCHED = 'LAUNCHED'
    FAILED = 'FAILED'
    KILLED = 'KILLED'
    ACTIVATED = 'ACTIVATED'
    DEACTIVATED = 'DEACTIVATED'
    REBALANCED = 'REBALANCED'
    STATES = (
        (LAUNCHED, 'Launched'),
        (FAILED, 'Failed'),
        (KILLED, 'Killed'),
        (ACTIVATED, 'Activated'),
        (DEACTIVATED, 'Deactivated'),
        (REBALANCED, 'Rebalanced'),
    )
    query = models.ForeignKey(BatchQuery, default='', null=True)
    user = models.ForeignKey(User)
    message = models.TextField(default='', null=True)
    state = models.CharField(max_length=10, choices=STATES)
    acked = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.query)+" @"+str(self.acked)

class BatchJobHistoryDetail(models.Model):
    job_history = models.ForeignKey(BatchJobHistory)
    message = models.TextField(default='', null=True)
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.job_history)+" @"+str(self.created)

