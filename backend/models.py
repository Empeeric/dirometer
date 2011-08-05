from django.db import models
import settings


####################Defines extended user class###################
class RentReport(models.Model):
    city=models.CharField(max_length=20,blank=False,null=False)
    street=models.CharField(max_length=20,blank=False,null=False)
    address=models.CharField(max_length=5,blank=False,null=False)
    apartment=models.CharField(max_length=5,blank=False,null=False)
    old_price=models.IntegerField(blank=False,null=True)
    new_price=models.IntegerField(blank=False,null=True)
    price_up=models.BooleanField(blank=False,null=False)
    lng=models.FloatField(null=True)
    lat=models.FloatField(null=True)








