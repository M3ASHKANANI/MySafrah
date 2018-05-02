from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['birthday', 'country', 'image', 'bio']

		widgets = {
			"birthday": forms.DateInput(attrs={"type":"date"}),
		}