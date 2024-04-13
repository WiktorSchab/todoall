from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import ProjectMember, ProjectTable, Project, ProjectTask
from .forms import NewProjectForm, NewProjectTableForm, TableTaskForm

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

@login_required(login_url="/login")
def singleproject(request, id):
	if request.method == 'POST':
		"""Adding new table"""
	
		project = Project.objects.filter(id=id).first()
		tables = ProjectTable.objects.filter(project=project).all()
		tables_count = tables.count()

		# Checking if project did not reach table limit
		if tables_count < 3:
			form = NewProjectTableForm(request.POST)
			if form.is_valid():
				table_new = form.save(commit=False)
				table_new.project = project
				table_new.save()
				
				messages.success(request, 'New table has been added succesfully the project.')
			else:
				messages.error(request, 'Error was encored. Project was not created.')
		else:
			messages.error(request, 'Project has reached table limit.')

		return redirect('singleproject', id)
	else:
		project = Project.objects.filter(id=id).first()
		tables = ProjectTable.objects.filter(project=project).all()
		members_list = ProjectMember.objects.filter(project=project).all()

		data = []
		for table in tables:
			tasks = ProjectTask.objects.filter(project_table=table, done=False).all()

			grouped_tasks = {}
			temp_tasks = []
			prev_date = ''
			for task in tasks:
				if prev_date == '':
					prev_date = task.date

				if prev_date == task.date:
					temp_tasks.append(task)
				else:
					grouped_tasks[prev_date] = temp_tasks
					prev_date = task.date

					temp_tasks = []
					temp_tasks.append(task)
			grouped_tasks[prev_date] = temp_tasks

			table_data = [table, grouped_tasks]

			data.append(table_data)


	context = {
		'project': project,
		'members_list':members_list,
		'data': data,
		'NewProjectTableForm': NewProjectTableForm,
		'form': TableTaskForm,
	}

	return render(request, 'singleproject.html', context)


"""Task control views"""
# Adding new task
@login_required(login_url="/login")
def singleproject_new(request, project_id):
	form = TableTaskForm(request.POST)

	if form.is_valid():
		task_new = form.save(commit=False)

		table = ProjectTable.objects.filter(id=form.cleaned_data['table_id']).first()
		project = Project.objects.filter(id=project_id).first()

		task_new.project = project
		task_new.project_table_id = table.id

		task_new.save()
		
	else:
		messages.error(request, 'An error occurred while creating a new task. The task was not created.')

	print(project_id)
	return redirect('singleproject', project_id)

# Marking task as done
@login_required(login_url="/login")
def singleproject_done(request, id):
	task = ProjectTask.objects.filter(id=id).first()
	task.done = True
	task.save()

	project_id = task.project_table.project.id
	return redirect('singleproject', project_id)

# Deleting task
@login_required(login_url="/login")
def singleproject_delete(request, id):
    task = ProjectTask.objects.filter(id=id).first()
    project_id = task.project_table.project.id

    task.delete()
    return redirect('singleproject', project_id)