from django.contrib.auth.models import User, Group, Permission
from help.models import *
from account.models import *
from system.models import *
from kafka import SimpleProducer, SimpleClient
import socket
import logging



def init_field_types():
    field_types = dict()
    field_types['text']=False
    field_types['textarea']=False
    field_types['dropdown']=True
    field_types['check']=False
    for key,value in field_types.iteritems():
        field_type = FieldType(field_type=key,has_options=value)
        field_type.save()

def init_job_titles():
    job_titles = (
        'Kanga Administrator',
        'Data Scientist',
        'Business Manager',
        'Software Engineer',
        'Head of Business',
        'Manufacturing Engineer',
        'Business Analyst',
        'Head of Software Engineer',
        'Head of Manufacturing Engineer',
    )
    for job in job_titles:
        job_title = JobTitle(job)
        job_title.save()

def init_user_groups():
    admin_group = Group(name="admin")
    admin_group.save()
    guest_group = Group(name="guest")
    guest_group.save()
    loop_index = 1
    permissions = Permission.objects.all()
    for permission in permissions:
        admin_group.permissions.add(permission)
        if loop_index > 18:
            guest_group.permissions.add(permission)
        loop_index += 1



def create_admin_user():
    user = User.objects.create_superuser(username='admin', first_name='', last_name='Administrator', email='bigdata@samsung.com', password='1')
    user.save()
    g = Group.objects.get(name='admin')
    g.user_set.add(user)
    job_title = JobTitle.objects.get(title='Kanga Administrator')
    user_detail = UserDetail.objects.create(user=user, activation_hashcode='',password_change_hashcode='',job_title=job_title)
    user_detail.save()

def create_guest_user():
    user = User.objects.create_user(username='guest', first_name='John', last_name='Doe', email='guest@samsung.com', password='1')
    user.save()
    g = Group.objects.get(name='guest')
    g.user_set.add(user)
    job_title = JobTitle.objects.get(title='Data Scientist')
    user_detail = UserDetail.objects.create(user=user, activation_hashcode='',password_change_hashcode='',job_title=job_title)
    user_detail.save()


def init_services():
    cluster = Cluster(name='Kanga Standalone Dev')
    cluster.save()
    node = Node(cluster=cluster,ip='127.0.0.1', hostname='localhost')
    node.save()




def main():
    init_field_types()
    init_job_titles()
    init_user_groups()
    create_admin_user()
    create_guest_user()
    init_services()    



main()

