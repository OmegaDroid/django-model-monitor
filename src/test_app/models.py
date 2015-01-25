from django.conf import settings
from django.db import models
from modelmonitor import monitor
import os


@monitor.changed
class MonitorAllFields(models.Model):
    first_field = models.IntegerField(default=0)
    second_field = models.IntegerField(default=0)


@monitor.changed("monitored_field")
class MonitorSomeFields(models.Model):
    monitored_field = models.IntegerField(default=0)
    unmonitored_field = models.IntegerField(default=0)


@monitor.changed
class AllFieldTypes(models.Model):
    big_int_field = models.BigIntegerField(default=0)
    int_field = models.IntegerField(default=0)
    bin_field = models.BinaryField(default=b"")
    bool_field = models.BooleanField(default=False)
    char_field = models.CharField(default="", max_length=20)
    csv_field = models.CommaSeparatedIntegerField(default="", max_length=20)
    date_field = models.DateField(default=None, null=True)
    date_time_field = models.DateField(default=None, null=True)
    decimal_field = models.DecimalField(default=0, decimal_places=2, max_digits=10, null=True)
    email_field = models.EmailField(default=None, null=True)
    file_field = models.FileField(upload_to=os.path.join(settings.BASE_DIR, "upload_to"), default=None, null=True)