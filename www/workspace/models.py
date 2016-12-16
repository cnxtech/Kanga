from django.db import models


class DashboardDetail(models.Model):

    dashboard_name = models.CharField(max_length=40)

    description = models.CharField(max_length=80, default='')

    parameters = models.CharField(max_length=1000)

    owner = models.CharField(max_length=30, default='')

