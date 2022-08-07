from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2","is_superuser")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class EditUserForm(UserChangeForm):
	email = forms.EmailField(required=True)
	
	class Meta:
		model = User
		fields = ("username", "email","is_superuser")

	def save(self, commit=True):
		user = super(EditUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class PdfForm(forms.ModelForm):
	pdf_file=forms.FileField()
	class Meta:
		model = User
		fields = ("username",)