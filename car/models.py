from django.db import models
import datetime


class CarsAll(models.Model):
    No = models.AutoField(primary_key=True)
    license_id = models.CharField(max_length=30)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True)
    image_path = models.CharField(max_length=100)

    def __str__(self):
        return self.license_id


class CarsIn(models.Model):
    license_id = models.CharField(max_length=30, primary_key=True)
    entry_time = models.DateTimeField()
