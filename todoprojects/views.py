from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import ProjectMember, ProjectTable, Project
from .forms import NewProjectForm

@login_required(login_url="/login")
def todoproject(request):
	if request.method == 'POST':
		form = NewProjectForm(request.POST)
		if form.is_valid():
			with transaction.atomic():
				# Creating new project
				project_new = form.save(commit=False)
				project_new.owner = request.user
				project_new.save()

				# Adding creator of project as member
				project_member = ProjectMember(project = project_new, user=request.user)
				project_member.save()
		else:
			messages.error(request, 'Error was encored. Project was not created.')
		return redirect('todoproject')
	
	projects = Project.objects.filter(projectmember__user=request.user)

	# Creating a list of projects along with their tables
	projects_with_table = []
	for project in projects:
		tables = ProjectTable.objects.filter(project=project)
		data_list = [project, tables]
		projects_with_table.append(data_list)

	form = NewProjectForm()

	context = {
		'NewProjectForm':form,
		'projects_with_table':projects_with_table,
	}
	return render(request, 'todoproject.html', context)
