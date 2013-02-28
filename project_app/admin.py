from project_app.models import Project, Ticket, Status
from django.contrib import admin

admin.site.register(Project)
admin.site.register(Ticket)
admin.site.register(Status)