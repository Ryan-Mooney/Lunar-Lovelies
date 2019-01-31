from django.db import models
from datetime import datetime

class products(models.Model):
	name=models.CharField(max_length=500, unique=True)
	picture_url=models.URLField(max_length=500)
	image1=models.ImageField(upload_to="images", default="images/no-image-found.png", null=True)
	image2=models.ImageField(upload_to="images", default="images/no-image-found.png", null=True)
	image3=models.ImageField(upload_to="images", default="images/no-image-found.png", null=True)
	image4=models.ImageField(upload_to="images", default="images/no-image-found.png", null=True)
	price=models.FloatField(default=0.00)
	category=models.CharField(max_length=1000)
	description=models.CharField(max_length=5000)
	filters=models.CharField(max_length=5000, default="None")
	date_added=models.DateTimeField(auto_now=True)
	paypal_button=models.CharField(max_length=5000)
	out_of_stock=models.BooleanField(default=False)

	objects=models.Manager()

	def __str__(self):
		return self.name
	def __unicode__(self):
		return self.name
