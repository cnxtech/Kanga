from django.db import models
from django.contrib.auth.models import Group, User
from datetime import datetime

class Role(models.Model):
    # Extending the Existing django-auth Group
    group = models.OneToOneField(Group)
    restrict_search_terms = models.CharField(max_length=50,default=100)
    restrict_search_timerange = models.IntegerField(default=-1)
    userlevel_concurrent_searchjobs_limit = models.IntegerField(default=3)
    Userlevel_concurrent_realtime_searchjobs_limit = models.IntegerField(default=6)
    rolelevel_concurrent_searchjobs_limit = models.IntegerField(default=50)
    rolelevel_concurrent_realtime_searchjobs_limit = models.IntegerField(default=100)
    limit_total_jobs_disk_quota = models.IntegerField(default=100)
    selected_roles = models.ManyToManyField('self')
    selected_indexes = models.CharField(max_length=50)
    selected_search_indexes = models.CharField(max_length=50)
    def __unicode__(self):
        return self.group.name


class JobTitle(models.Model):
    title = models.CharField(max_length=50,primary_key=True)
    def __unicode__(self):
        return self.title


class UserDetail(models.Model):
    # Extending the Existing django auth User
    user = models.OneToOneField(User)
    activation_hashcode = models.CharField(max_length=50, default='', blank=True)
    password_change_hashcode = models.CharField(max_length=50, default='', blank=True)
    job_title = models.ForeignKey(JobTitle,default='Kanga Administrator')
    def __unicode__(self):
        return self.user.username


class UserActivation(models.Model):
    username = models.CharField(max_length=50)
    activation_hashcode = models.CharField(max_length=50)
    passwordchange_hashcode = models.CharField(max_length=50)
    # active_user = models.BooleanField()
    def __unicode__(self):
        return self.username

