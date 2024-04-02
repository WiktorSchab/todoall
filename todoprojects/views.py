from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import ProjectMember
from .forms import NewProjectForm

@login_required(login_url="/login")
def todoproject(request):
	if request.method == 'POST':
		form = NewProjectForm(request.POST)
		if form.is_valid():
			with transaction.atomic():
				project_new = form.save(commit=False)
				project_new.owner = request.user
				project_new.save()

				project_member = ProjectMember(project = project_new, user=request.user)
				project_member.save()
		else:
			messages.error(request, 'Error was encored. Project was not created.')

		return redirect('todoproject')

	form = NewProjectForm()

	context = {
		'NewProjectForm':form,
	}
	return render(request, 'todoproject.html', context)
