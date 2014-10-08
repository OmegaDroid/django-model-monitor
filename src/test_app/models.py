from django.db import models
from modelmonitor import monitor


@monitor.changed
class MonitorAllFields(models.Model):
    first_field = models.IntegerField(default=0)
    second_field = models.IntegerField(default=0)


@monitor.changed("monitored_field")
class MonitorSomeFields(models.Model):
    monitored_field = models.IntegerField(default=0)
    unmonitored_field = models.IntegerField(default=0)
