from django.db import models
from django.contrib.auth.models import User

class Domain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=512, verbose_name="Domain")
    limit = models.IntegerField()


class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    domain = models.ForeignKey(Domain, on_delete=models.PROTECT, null=True)
    query = models.CharField(max_length=8048, verbose_name="Query")
    position = models.IntegerField()
    frequency = models.IntegerField()
    region = models.CharField(max_length=32, verbose_name="Region", null=True)