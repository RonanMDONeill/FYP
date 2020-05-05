from django.db import models

# Create your models here.
class RecPub(models.Model):
	paperID = models.IntegerField()
	text = models.CharField(max_length=500)
