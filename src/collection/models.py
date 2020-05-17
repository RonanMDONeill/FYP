from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 

# Define the models for the Collection app
class Collection(models.Model):
	# Use ForeignKey to link a user and a collection
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collection")
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Publication(models.Model):
	# Use all the properties of the Neo4j Publication mode
	paperID = models.IntegerField()
	title = models.CharField(max_length=240)
	authorNames = models.CharField(max_length=240)
	authorIDs = models.CharField(max_length=240)
	year = models.PositiveSmallIntegerField(null=True, blank=True)
	fos = models.CharField(max_length=120, null=True, blank=True)
	references = models.CharField(max_length=120, null=True, blank=True)
	doi = models.URLField(null=True, blank=True)
	venueName = models.CharField(max_length=120, null=True, blank=True)
	publisher = models.CharField(max_length=120, null=True, blank=True)
	n_citation = models.CharField(max_length=50, null=True, blank=True)

class Author(models.Model):
	# Use all the properties of the Neo4j Author mode
	authorID = models.IntegerField()
	authorName = models.CharField(max_length=240)
	authorOrg = models.CharField(max_length=240, null=True, blank=True)
	coAuthors = models.CharField(max_length=240, null=True, blank=True)

class ItemList(models.Model):
	# Link a publication to a collection using ForeignKeys
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
	publication = models.ForeignKey(Publication, null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.collection.name

class PubRating(models.Model):
	# Link a rating to a publication and user using ForeignKeys
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating")
	publication = models.ForeignKey(Publication, null=True, blank=True, on_delete=models.CASCADE)

	# Set the rating
	rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

	name = str(User) + " - " + str(Publication.title)

	def __str__(self):
		return self.name
