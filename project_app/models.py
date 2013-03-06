from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from djangop.utils.encoding import iri_to_uri
from django.forms import ModelForm
from django import forms


class Project(models.Model):
	name = models.CharField(max_length = 50)
	description = models.TextField()
	start_date = models.DateField('Start date')
	end_date = models.DateField('End date')
	date_added = models.DateField()
	date_updated = models.DateField()
	added_by_user = models.ForeignKey(User)
	users = models.ManyToManyField(User, related_name='projects')

	def __unicode__(self):
		return self.name

	def owned_by_user(self, user):
		return self.added_by_user == user


class Status(models.Model):
	status_name = models.CharField(max_length = 50)

	def __unicode__(self):
		return self.status_name


class Ticket(models.Model):
	name = models.CharField(max_length = 50)
	description = models.TextField()
	start_date = models.DateField('date result published')
	end_date = models.DateField('date result published')
	date_added = models.DateField()
	date_updated = models.DateField()
	status = models.ForeignKey(Status, related_name="projects")
	project = models.ForeignKey(Project, related_name="projects")
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.name

	def owned_by_user(self, user):
		return self.user == user


class ProjectForm(ModelForm):
	class Meta:
		model = Project
		exclude = ('date_added', 'date_updated', 'added_by_user')


class TicketForm(ModelForm):
	class Meta:
		model = Ticket
		exclude = ('date_added', 'date_updated', 'project', 'user')


class ChangeTicketStatusForm(ModelForm):
	class Meta:
		model = Ticket
		exclude = ('name', 'description', 'start_date', 'end_date', 'date_added', 'date_updated', 'project', 'user')


class LoginForm(forms.Form):
	username = forms.CharField(max_length = 20)
	password = forms.CharField(max_length = 20, widget = forms.PasswordInput)