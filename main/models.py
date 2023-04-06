from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RegionModel(models.Model):
    region = models.CharField(max_length=32, verbose_name="Region")
    number = models.IntegerField()


class KeyXmlProxy(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, unique=True)
    email = models.CharField(max_length=2048, verbose_name="Email", null=True)
    key = models.CharField(max_length=2048, verbose_name="Key")

