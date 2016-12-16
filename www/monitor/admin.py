from django.contrib import admin
from monitor.models import *

# Register your models here.
admin.site.register(StreamingJobHistory)
admin.site.register(StreamingJobHistoryDetail)
admin.site.register(BatchJobHistory)
admin.site.register(BatchJobHistoryDetail)
