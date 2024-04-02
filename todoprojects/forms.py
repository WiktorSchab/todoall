from django import forms
from .models import Project

class NewProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ('name',)

	def __init__(self, *args, **kwargs):
		super(NewProjectForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = ''
