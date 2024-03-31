from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import LoginForm, SignUpForm, PrivateTaskForm
from .models import PrivateTask, BaseTask
import datetime
import uuid

def home(request):
	return render(request, 'home.html')


def login_user(request):
	if request.method == 'POST':  
		form = LoginForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			messages.success(request, 'You have been successfully logged in.')
			return redirect('home')
	else:
		form = LoginForm()

	context = {
		'form': form,
		'redirect_to': 'login',
	}
	return render(request, 'login_register.html', context)

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Your account has been successfully created. You have been logged in.')
			return redirect('home')
	else: 
		form = SignUpForm()    

	context = {
		'form':form,
		'redirect_to': 'register',
	}
	return render(request, 'login_register.html', context)

def logout_user(request):
	logout(request)
	messages.success(request, 'Logout was successful')
	return redirect('home')

def mytodo(request):
	if request.method == 'POST':
		# Creating a form based on data submitted via POST method
		form = PrivateTaskForm(request.POST)

		if form.is_valid():
			# Getting clean data from the form
			title = form.cleaned_data.get('title')
			description = form.cleaned_data.get('description')
			date = form.cleaned_data.get('date')
			hour = form.cleaned_data.get('hour')
			color = form.cleaned_data.get('color')
			done = False

			next_id = len(request.session.get('private_tasks', [])) + 1
			task_id = str(uuid.uuid4())

			# Checking if the user is logged in
			if request.user.is_authenticated:
				# If the user is logged in, save the form to the database
				private_task = form.save(commit=False)
				private_task.owner = request.user
				private_task.save()
			else:
				# If the user is not logged in, save the data in the session
				if 'private_tasks' not in request.session:
					request.session['private_tasks'] = [] 

				# Creating a dictionary containing task data
				data = {
					'id':task_id,
					'title':title,
					'description':description,
					'color':color,
					'date':date.isoformat(),
					'hour':hour.isoformat(),
					'done':done,
				}

				# Adding task data to the session
				request.session['private_tasks'].append(data)

				# Marking the session as modified
				request.session.modified = True
   
		return redirect('mytodo')
	else:    
		form = PrivateTaskForm()

		# Checking if the user is logged in
		if request.user.is_authenticated:
			tasks_ended = PrivateTask.objects.filter(owner=request.user, date__lt=datetime.date.today(), done=False).order_by('date')
			tasks = PrivateTask.objects.filter(owner=request.user, date__gte=datetime.date.today(), done=False).order_by('date')
		else:
			# Creating querysets with annonymous user to have same data structure when user is logged or not
			anonymous_user = User.objects.get(username='anonymous')
			tasks = []
			tasks_ended = []

			private_tasks_data = request.session.get('private_tasks', [])
			for task_data in private_tasks_data:
				task_date = datetime.datetime.strptime(task_data['date'], '%Y-%m-%d').date()

				hour, minute, second = map(int, task_data['hour'].split(':'))
				hour_time = datetime.time(hour=hour, minute=minute, second=second)

				private_task = PrivateTask(
					id=task_data['id'],
					owner=anonymous_user,
					title=task_data['title'],
					description=task_data['description'],
					color=task_data['color'],
					date=task_date,
					hour=hour_time,
					done=task_data['done'],
				)

				if private_task.done == False:
					if private_task.date < datetime.date.today():
						tasks_ended.append(private_task)
					else:
						tasks.append(private_task)

		# Simple algoritm to group tasks by date
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

	context = {
		'form': form,
		'tasks_ended':tasks_ended,
		'grouped_tasks':grouped_tasks,
	}

	return render(request, 'mytodo.html', context)

def delete_task(request, id):
	if request.user.is_authenticated:
		PrivateTask.objects.filter(id=id).delete()
	else:
		private_tasks = request.session.get('private_tasks', [])

		for task in private_tasks:
			if task.get('id') == id:
				private_tasks.remove(task)
				request.session['private_tasks'] = private_tasks
				break
		request.session.modified = True
	return redirect('mytodo') 

def complete_task(request, id):
	if request.user.is_authenticated:
		PrivateTask.objects.filter(id=id).update(done=True)
	else:
		private_tasks = request.session.get('private_tasks', [])

		for task in private_tasks:
			if task.get('id') == id:
				task['done'] = True
				request.session['private_tasks'] = private_tasks
				break
		request.session.modified = True

	return redirect('mytodo') 