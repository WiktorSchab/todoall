from django import forms
from .models import Project, ProjectTable, ProjectTask
from core.forms import RadioSelectNoLabel

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


class TableTaskForm(forms.ModelForm):
	# Hidden field that will contain table id
    table_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = ProjectTask
        fields = ['title', 'description', 'date', 'hour', 'color']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hour': forms.DateInput(attrs={'type': 'time'}),
            'color': RadioSelectNoLabel(choices=ProjectTask.COLOR_CHOICES),
        }
		
    def __init__(self, *args, **kwargs):
        super(TableTaskForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label 
            field.label = False

        self.fields['color'].choices = [(value, label) for value, label in ProjectTask.COLOR_CHOICES[:]]

