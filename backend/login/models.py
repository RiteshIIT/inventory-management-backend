from django.contrib.auth.models import User
from django.db import models

class Inventory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    code=models.CharField(max_length=3)
    quantity=models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
