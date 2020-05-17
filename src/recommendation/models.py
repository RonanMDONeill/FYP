from django.db import models

# Define the models for the Recommendation app
class RecPub(models.Model):
	# Properties for thr RecPub are the Paper ID and the corresponding text data (i.e. title, fos names, abstract)
	paperID = models.IntegerField()
	text = models.CharField(max_length=500)
