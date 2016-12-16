from django.contrib import admin
from system.models import *

# Register your models here.
admin.site.register(Cluster)
admin.site.register(Node)
admin.site.register(Service)
admin.site.register(DatabaseService)
admin.site.register(Config)
admin.site.register(JobScript)
admin.site.register(ConnectedDevice)
