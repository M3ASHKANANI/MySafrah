from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Traveltype(models.Model):
	# solo = models.BooleanField(default=True)
	# family = models.BooleanField(default=True)
	# backpack = models.BooleanField(default=True)
	# business = models.BooleanField(default=True)
	# couple = models.BooleanField(default=False)
	# Friends = models.BooleanField(default=False)
	# medical = models.BooleanField(default=False)
	title = models.CharField(max_length=120)

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
	
	def __str__(self):
		return self.owner



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
	hotel = models.BooleanField()
	location = models.BooleanField()
	posttraveltype = models.ManyToManyField(Traveltype, related_name="posttraveltype") 
	description = models.CharField(max_length=250)
	rate = models.BooleanField()
	suitablefor = models.ManyToManyField(Traveltype, related_name="suitablefor") 
	established = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.description

# class Hotel(models.Model):
# 	city = 
# 	name =
# 	image = 

	