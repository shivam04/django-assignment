from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
from .models import DataFeed
from pagedown.widgets import PagedownWidget


User = get_user_model()
class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username,password=password)
			if not user:
				raise forms.ValidationError("This User Doesn't Exist")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("User is no longer active.")
		return super(UserLoginForm, self).clean(*args, **kwargs)

class DataFeedForm(forms.ModelForm):
	input_text = forms.CharField(widget=PagedownWidget(show_preview=False))
	class Meta:
		model = DataFeed
		fields = [
			'input_text',
		]


class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email address')
	email2 = forms.EmailField(label='Confirm Email')
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model=User
		fields = [
		'username',
		'email',
		'email2',
		'password',
		'first_name',
		'last_name',
		'is_staff',
		]
	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Emails Must Match!")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This Email has already been registered!")
		return email