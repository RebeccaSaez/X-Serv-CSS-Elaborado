from django.db import models

# Create your models here.


class Table(models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
