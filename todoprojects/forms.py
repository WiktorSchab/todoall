from django import forms
from .models import Project, ProjectTable

class NewProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ('name',)

	def __init__(self, *args, **kwargs):
		super(NewProjectForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = ''


class NewProjectTableForm(forms.ModelForm):
	class Meta:
		model = ProjectTable
		fields = ('name',)

	def __init__(self, *args, **kwargs):
		super(NewProjectTableForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = ''
