from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['birthday', 'country', 'image', 'bio', 'travelpref']

		widgets = {
			"birthday": forms.DateInput(attrs={"type":"date"}),
			"travelpref": forms.CheckboxSelectMultiple(),
		}


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['image','hotel','country','city','posttraveltype','description','rate','suitablefor','facility']

		widgets = {
			"posttraveltype": forms.CheckboxSelectMultiple(),
			"suitablefor": forms.CheckboxSelectMultiple(),
			"facility": forms.CheckboxSelectMultiple(),
		}


# class HotelForm(forms.ModelForm):
# 	class Meta:
# 		model = 