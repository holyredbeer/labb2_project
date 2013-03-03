from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from project_app.models import Project, Ticket, ProjectForm, TicketForm, LoginForm
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


#####
# Home method
#####
@login_required
def home(request):
	return render(request, 'index.html')


#####
# List all projecs
#####
@login_required
def project_list(request):
	projects = get_list_or_404(Project.objects.order_by('name'))
	return render(request, 'projects/list.html', {"projects" : projects, "headline" : "All projects"})

#####
# Show a specific project
#####
@login_required
def show_project(request, project_id):
	project = get_object_or_404(Project, pk = project_id)
	tickets = Ticket.objects.filter(project_id = project_id)

	return render(request, 'projects/show.html', {"project" : project, "tickets" : tickets})


#####
# Show a specific user's projects
#####
@login_required
def projects_for_user(request):
	user = request.user
	projects = get_list_or_404(Project.objects.filter(added_by_user = user))
	return render(request, 'projects/list.html', {"projects" : projects, "headline" : "Your projects"})


#####
# Add a new project
#####
@login_required
def project_add(request):
	if request.method == "POST":
		form = ProjectForm(request.POST)
		if form.is_valid():
			form.instance.date_added = datetime.date.today()
			form.instance.date_updated = datetime.date.today()
			form.instance.added_by_user = request.user
			form.save()
			return redirect(project_list)
	else:
		form = ProjectForm()

	return render(request, 'projects/add.html', {"form" : form})


#####
# Edit a new project
#####
@login_required
def project_edit(request, project_id):
	project = get_object_or_404(Project, pk = project_id)

	if project.owned_by_user(request.user):
		if request.method == "POST":
			form = ProjectForm(request.POST, instance = project)
			if form.is_valid():
				try:
					form.save()
					return redirect('project_list')
				except:
					return HttpResponseServerError()
		else:
			form = ProjectForm(instance = project)
	else:
		return HttpResponse("You don't own this project")
	return render(request, 'projects/add.html', {"form": form}) #, "value" : "Update project"})


#####
# Delete a project
#####
@login_required
def project_delete(request, project_id):
	project = get_object_or_404(Project, pk = project_id)

	if project.owned_by_user(request.user):
		project.delete()
		return redirect('project_list') # <- andra till projects_for_user
	else:
		return HttpResponse("Permissions denied")


#####
# Show a project's all tickets
#####
@login_required
def ticket_list(request, project_id):
	tickets = get_list_or_404(Project.objects.order_by('name'))
	return render(request, 'projects/tickets.html', {"tickets" : tickets, "headline" : "All tickets"})


#####
# Show a specific ticket
#####
@login_required
def show_ticket(request, ticket_id, project_id):
	ticket = get_object_or_404(Ticket, pk = ticket_id)
	project = get_object_or_404(Project, pk = project_id)

	return render(request, 'projects/show_ticket.html', {"ticket" : ticket, "project" : project})


#####
# Add a new ticket
#####
@login_required
def ticket_add(request, project_id):
	if request.method == "POST":
		form = TicketForm(request.POST)
		if form.is_valid():
			form.instance.date_added = datetime.date.today()
			form.instance.date_updated = datetime.date.today()
			form.instance.project_id = project_id
			form.instance.user = request.user
			form.save()
			return redirect(project_list)
	else:
		form = TicketForm()

	return render(request, 'projects/add.html', {"form" : form})


#####
# Login user
#####
def login_user(request):
	message = ''
	if request.method == "POST":

		form = LoginForm(request.POST)
		if form.is_valid():
			username_to_try = form.cleaned_data["username"]
			password_to_try = form.cleaned_data["password"]

			user = authenticate(username = username_to_try, password = password_to_try)
			if user is not None:
				if user.is_active:
					login(request, user)
					#request.session['has_logged_in'] = True
					return redirect('projects_for_user')
				else:
					return HttpResponse("<h1>Your account is disabled</h1>")
			else:
				message = "Wrong username or password"
	else:
		form = LoginForm()
	return render(request, 'login.html', {'form' : form, 'message' : message})


#####
# Logout user
#####

def logout_user(request):
	logout(request)
	return redirect('login')


#####
# Redirect to /projects/ if /project/
#####

def goto_projects(request):
	return redirect('project_list')