from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator

class Traveltype(models.Model):
	title = models.CharField(max_length=120)
	

	def __str__(self):
		return self.title

# class FacilityRate(models.Model):
	# facrate = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

class Facility(models.Model):
	title = models.CharField(max_length=120)
	# facrate = models.ManyToManyField(FacilityRate) 

	def __str__(self):
		return self.title


class Profile(models.Model):
	owner = models.OneToOneField(User, on_delete=models.CASCADE)
	birthday = models.DateField(auto_now=False, auto_now_add=False)
	country = CountryField()
	travelpref = models.ManyToManyField(Traveltype)
	image = models.ImageField(null=True, blank=True)
	established = models.DateField(auto_now_add=True)
	bio = models.CharField(max_length=350)
	



class Follow(models.Model):
	# stalker will give me who I'm following
	stalker = models.ForeignKey(User, related_name="stalker", on_delete=models.CASCADE)
	# prey will give me who is following me
	prey = models.ForeignKey(User, related_name="prey", on_delete=models.CASCADE)

class Clue(models.Model):
	message = models.CharField(max_length=255)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-timestamp']

class Favorite(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	clue = models.ForeignKey(Clue, on_delete=models.CASCADE, related_name="favorites")



class Post(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	image = models.ImageField(null=True, blank=True)
	hotel = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	posttraveltype = models.ManyToManyField(Traveltype, related_name="posttraveltype") 
	description = models.CharField(max_length=250)
	rate = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
	suitablefor = models.ManyToManyField(Traveltype, related_name="suitablefor") 
	established = models.DateField(auto_now_add=True)
	facility = models.ManyToManyField(Facility)

	def __str__(self):
		return self.description


# class Hotel(models.Model):
# 	city = 
# 	name =
# 	image = 

	