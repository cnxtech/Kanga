from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

class RegistryHistory(models.Model):
    library_id = models.CharField(max_length=50)  # name + "_" + version
    package_location = models.CharField(max_length=200,default='')
    package_filename = models.CharField(max_length=100,default='')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    description = models.TextField(default='')

class Library(models.Model):
    BASE_LIBRARY_TYPE = 'BASE_LIBRARY'
    THIRD_PARTY_LIBRARY_TYPE = 'THIRD_PARTY_LIBRARY'
    LIBRARY_TYPE_CHOICES = (
        (BASE_LIBRARY_TYPE, 'Base Library'),
        (THIRD_PARTY_LIBRARY_TYPE, 'Third Party Library')
    )
    id = models.CharField(max_length=50,primary_key=True)   # name + "_" + version
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=50)
    package_location = models.CharField(max_length=200,default='')
    package_filename = models.CharField(max_length=100,default='')
    created = models.DateTimeField(auto_now_add=True)
    library_type = models.CharField(max_length=6,
                                 choices=LIBRARY_TYPE_CHOICES,
                                 default=BASE_LIBRARY_TYPE)
    user = models.ForeignKey(User)
    description = models.TextField(default='')
    def __unicode__(self):
        return self.id

class JarFile(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    jar_file = models.CharField(max_length=100, primary_key=True)
    def __unicode__(self):
        return self.jar_file

class Category(models.Model):
    category = models.CharField(max_length=30, primary_key=True)
    category_text = models.CharField(max_length=200)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.category_text


class Command(models.Model):
    SOURCE_TYPE = 'SOURCE'
    SINK_TYPE = 'SINK'
    JOIN_TYPE = 'JOIN'
    NORMAL_TYPE = 'NORMAL'
    EMPTY = 'NA'
    NODE_TYPE_CHOICES = (
        (SOURCE_TYPE, 'Source'),
        (SINK_TYPE, 'Sink'),
        (JOIN_TYPE, 'Join'),
        (NORMAL_TYPE, 'Normal'),
        (EMPTY, 'Na')
    )
    BOLT = 'BOLT'
    SPOUT = 'SPOUT'
    STORM_NODE_TYPE_CHOICES = (
        (BOLT, 'Bolt'),
        (SPOUT, 'Spout'),
    )
    category = models.ForeignKey(Category, default='', null=True, on_delete=models.CASCADE)
    md_file = models.CharField(max_length=200)
    command = models.CharField(max_length=200, primary_key=True)
    bolt_name = models.CharField(max_length=100, default='')
    node_type = models.CharField(max_length=6,
                                 choices=NODE_TYPE_CHOICES,
                                 default=NORMAL_TYPE)
    storm_node_type = models.CharField(max_length=5,
                                       choices=STORM_NODE_TYPE_CHOICES,
                                       default=BOLT)
    def __unicode__(self):
        return str(self.command)+" ["+str(self.node_type)+"]"



class FieldType(models.Model):
    field_type = models.CharField(max_length=20, primary_key=True)
    has_options = models.BooleanField(default=False)
    def __unicode__(self):
        return self.field_type


class Field(models.Model):
    id = models.CharField(max_length=200, primary_key=True) # id=command+"_"+field_name as surrogate_key
    command = models.ForeignKey(Command, null=True, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=200, default='')
    field_type = models.ForeignKey(FieldType, default='',null=True)
    default_value = models.CharField(max_length=100, null=True, blank=True, default='')
    is_mandatory = models.BooleanField(default=True)
    placeholder = models.CharField(max_length=100, default='')
    def __unicode__(self):              # __str__ on Python 3
        return self.command.command + ', ' + self.field_name


class Option(models.Model):
    id = models.CharField(max_length=200, primary_key=True) # id = command + "_" + field_name + "_" + option_value
    field = models.ForeignKey(Field,null=True, on_delete=models.CASCADE)
    option_value = models.CharField(max_length=200)
    def __unicode__(self):
        return str(self.field) + ", " + str(self.option_value)
        # return self.id

