
from django.db import models
from django.contrib.auth.models import User

class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

class Paybill(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)

class QRCode(models.Model):
    paybill = models.ForeignKey(Paybill, on_delete=models.CASCADE)
    code = models.TextField()
