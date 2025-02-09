from django.contrib.auth.models import User
from django.db import models

class Inventory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    img = models.TextField()
    quantity=models.IntegerField()
    price=models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

