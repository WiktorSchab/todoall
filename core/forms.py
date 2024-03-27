from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import PrivateTask

class RadioSelectNoLabel(forms.RadioSelect):
	def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
		option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
		option['label'] = ''
		return option


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['email'].widget.attrs['placeholder'] = 'Email'

		self.fields['username'].widget.attrs['placeholder'] = 'Username'
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
		

class LoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['placeholder'] = 'Username'
		self.fields['password'].widget.attrs['placeholder'] = 'Password'



class PrivateTaskForm(forms.ModelForm):
	class Meta:
		model = PrivateTask
		fields = ['title', 'description', 'date', 'hour', 'color']
		widgets = {
			'date': forms.DateInput(attrs={'type': 'date'}),
			'hour': forms.DateInput(attrs={'type': 'time'}),
			'color': RadioSelectNoLabel(choices=PrivateTask.COLOR_CHOICES),
		}
		
	def __init__(self, *args, **kwargs):
		super(PrivateTaskForm, self).__init__(*args, **kwargs)

		# Deleting labels from fields
		for field_name, field in self.fields.items():
			field.widget.attrs['placeholder'] = field.label 
			field.label = False

		# Deleting empty option in color field
		self.fields['color'].choices = [(value, label) for value, label in PrivateTask.COLOR_CHOICES[:]]

		for choice_value, choice_label in PrivateTask.COLOR_CHOICES:
			print(self.fields['color'])



		

		
