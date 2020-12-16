from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to ="uploadImgs/") 
    label = models.CharField(max_length=20, null=True,blank=True)
    probability = models.FloatField(null=True,blank=True)
