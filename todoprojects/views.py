from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
import json

from django.contrib.auth.models import User
from .models import ProjectMember, ProjectTable, Project, ProjectTask, Notification
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

	notifications = Notification.objects.filter(receiver=request.user).all

	context = {
		'NewProjectForm':form,
		'projects_with_table':projects_with_table,
		'notifications':notifications,
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


# Handles AJAX requests for adding new users to project.
def add_user(request):
	# Loading data from ajax req
	data = json.loads(request.body)
	
	project_id = data.get('projectID')
	user = data.get('user')

	user_obj  = User.objects.filter(username=user).first()

	# Checking if user exists
	if not user_obj:
		return JsonResponse({'req_status': 'That user does not exists'})
	
	project = Project.objects.filter(id=project_id).first()
	
	# Checking if user is part of project already
	if ProjectMember.objects.filter(project=project, user=user_obj).exists():
		return JsonResponse({'req_status': 'That user is already part of project'})


	if Notification.objects.filter(receiver=user_obj, notification='invited', project=project).exists():
		return JsonResponse({'req_status': 'That user already received invitation to the project.'})
	

	# Creating record & saving it
	notification = Notification.objects.create(
		sender=request.user,
		receiver=user_obj,
		notification='invited', 
		project=project
	)
	notification.save()

	return JsonResponse({'req_status': 'User has been invited'})


# Handles AJAX requests for accepting/decling invite
def decision_invite(request):
	# Loading data from ajax req
	data = json.loads(request.body)

	notification_id = data.get('notificationID')
	decision = data.get('decision')
	
	notification = Notification.objects.filter(id=notification_id).first()

	if decision == 'deny':
		notification_decline = Notification.objects.create(
			sender=request.user,
			receiver=notification.sender,
			notification='declined', 
			project=notification.project
		)
		notification.save()
	else:
		project = notification.project
		user_add = notification.receiver

		# Adding user only if he is not already part of project
		if not ProjectMember.objects.filter(project=project, user=user_add).exists():
			project_member = ProjectMember.objects.create(project=project, user=user_add)
			project_member.save()

			notification_decline = Notification.objects.create(
				sender=request.user,
				receiver=notification.sender,
				notification='accepted', 
				project=notification.project
			)
			notification.save()
		else:
			print('User was already part of project')

	notification.delete()

	return JsonResponse({'req_status': 'Request returned'})