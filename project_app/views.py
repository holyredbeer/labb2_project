from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from project_app.models import Project, Ticket, ProjectForm, TicketForm, LoginForm, ChangeTicketStatusForm
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseServerError
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
# List filtered projecs
#####
@login_required
def project_list_filtered(request, projects_to_show):
	if projects_to_show == 'admin':
		projects = get_list_or_404(Project.objects.filter(added_by_user = request.user))
		headline = "Your projects"
	else:
		if projects_to_show == 'member':
			projects = get_list_or_404(Project.objects.filter(users__id__iexact=request.user.id))
			headline = "Projects you're are a member of"
		else:
			if projects_to_show == 'nonmember' :
				projects = Project.objects.exclude(users__id__iexact=request.user.id)
				projects = projects.exclude(added_by_user = request.user)
				headline = "Projects that you're not a member or admin of"
			else:
				headline = "All projects"
				projects = get_list_or_404(Project.objects.order_by('name'))

	return render(request, 'projects/list.html', {"projects" : projects, "headline" : headline})

#####
# Show a specific project
#####
@login_required
def show_project(request, project_id):
    project = get_object_or_404(Project, pk = project_id)
    tickets = Ticket.objects.filter(project_id = project_id)
    if request.user in project.users.all() or project.owned_by_user(request.user):
        return render(request, 'projects/show.html', {"project" : project, "tickets" : tickets})
    else:
        return render(request, 'projects/show.html', {"error_message": "You don't have permission to view the project"})


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
# Manage projects
#####
@login_required
def project_manage(request):
	projects = get_list_or_404(Project.objects.filter(added_by_user = request.user))

	return render(request, 'projects/manage.html', {"projects" : projects, "headline" : "Manage projects"})


#####
# Edit a project
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
					return redirect('project_manage')
				except:
					return HttpResponseServerError()
		else:
			form = ProjectForm(instance = project)
	else:
		return render(request, 'projects/edit.html', {"error_message": "You don't have permission to view the project"})
	return render(request, 'projects/edit.html', {"form": form}) #, "value" : "Update project"})


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
#@login_required
#def ticket_list(request, project_id):
#	tickets = get_list_or_404(Project.objects.order_by('name'))
#	return render(request, 'projects/tickets.html', {"tickets" : tickets, "headline" : "All tickets"})

#####
# Show a project's all tickets
#####
@login_required
def users_tickets(request):
	tickets = get_list_or_404(Ticket.objects.filter(user = request.user.id))

	return render(request, 'tickets/list.html', {"tickets" : tickets, "headline" : "Your tickets"})


#####
# Show a specific ticket
#####
@login_required
def show_ticket(request, ticket_id, project_id):
	ticket = get_object_or_404(Ticket, pk = ticket_id)
	project = get_object_or_404(Project, pk = project_id)
	form = ''

	if ticket.owned_by_user(request.user) or project.owned_by_user(request.user):
		if ticket.owned_by_user(request.user):
			if request.method == "POST":
				form = ChangeTicketStatusForm(request.POST, instance = ticket)
				if form.is_valid():
					try:
						form.save()
					except:
						return HttpResponseServerError()
			else:
				form = ChangeTicketStatusForm(instance = ticket)

		return render(request, 'tickets/show.html', {"ticket" : ticket, "project" : project, "form": form})
	else:
		return render(request, 'tickets/show.html', {"error_message": "You don't have permission to view the ticket"})


#####
# Add a new ticket
#####
@login_required
def ticket_add(request, project_id):

	project = get_object_or_404(Project, pk = project_id)
	if request.user in project.users.all() or project.owned_by_user(request.user):
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

		return render(request, 'tickets/add.html', {"form" : form})

	else:
		return render(request, 'tickets/add.html', {"error_message": "You don't have permission to add a ticket to this project"})


#####
# Edit a ticket
#####
@login_required
def ticket_edit(request, ticket_id, project_id):
	ticket = get_object_or_404(Ticket, pk = ticket_id)

	if ticket.owned_by_user(request.user):
		if request.method == "POST":
			form = TicketForm(request.POST, instance = ticket)
			if form.is_valid():
				try:
					form.save()
					return redirect('users_tickets')
				except:
					return HttpResponseServerError()
		else:
			form = TicketForm(instance = ticket)
	else:
		return render(request, 'tickets/edit.html', {"error_message": "You don't own the ticket or the project that the ticket belongs to"})

	return render(request, 'tickets/edit.html', {"form": form}) #, "value" : "Update project"})


#####
# Delete a ticket
#####
@login_required
def ticket_delete(request, ticket_id):
	ticket = get_object_or_404(Ticket, pk = ticket_id)

	if ticket.owned_by_user(request.user):
		ticket.delete()
		return redirect('users_tickets') # <- andra till projects_for_user
	else:
		return HttpResponse("Permissions denied")


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
					return redirect('home')
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