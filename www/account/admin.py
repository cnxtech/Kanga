from django.contrib import admin
from account.models import *

admin.site.register(UserDetail)
admin.site.register(Role)
admin.site.register(JobTitle)
admin.site.register(UserActivation)