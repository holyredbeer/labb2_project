from django.db import models
from django.contrib.auth.models import User
# from djangop.utils.encoding import iri_to_uri
# from django.forms import Modelforms


class Project(models.Model):
	added_by_user = models.ForeignKey(User, related_name='projects')
	users = models.ManyToManyField(User)
	name = models.CharField(max_length = 50)
	description = models.TextField()
	start_date = models.DateTimeField('date result published')
	end_date = models.DateTimeField('date result published')
	date_added = models.DateField()
	date_updated = models.DateField()

	def __unicode__(self):
		return self.name


class Status(models.Model):
	status_name = models.CharField(max_length = 50)

	def __unicode__(self):
		return self.status_name


class Ticket(models.Model):
	name = models.CharField(max_length = 50)
	description = models.TextField()
	start_date = models.DateTimeField('date result published')
	end_date = models.DateTimeField('date result published')
	date_added = models.DateField()
	date_updated = models.DateField()
	status = models.ForeignKey(Status, related_name="projects")
	project = models.ForeignKey(Project, related_name="projects")
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.name


# class ProjectModel(ModelForm):
