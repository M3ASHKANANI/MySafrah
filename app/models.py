from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# #
# class Profile(models.Model):
# 	owner = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.TextField()
#     birthday = models.DateField(auto_now=False, auto_now_add=False)
#     country = CountryField()
#     travelpref = models.ForeignKey(Travelpref, )
# 	image = models.ImageField(null=True)
# 	established = models.DateField(auto_now_add=True)
# 	bio = models.CharField(max_length=350)
# #
# #
# #
#
# class Post(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     title = models.TextField()
#     image = models.ImageField(null=True)
#     hotel = # from google API
#     suitablefor =
#     commint =
#     rate =
#     established = models.DateField(auto_now_add=True)
#     traveltype =
# #
# class Travelpref(models.Model):
# 	solo = models.Boole
#
#
#
#
#
#
# class Follow(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
# 	def __str__(self):
# 		return self.profile.owner.username
