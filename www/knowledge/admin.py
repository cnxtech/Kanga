from django.contrib import admin
from knowledge.models import *

# Register your models here.
admin.site.register(RealtimeQuery)
admin.site.register(RealtimeQueryPermission)
admin.site.register(BatchQuery)
admin.site.register(BatchQueryPermission)