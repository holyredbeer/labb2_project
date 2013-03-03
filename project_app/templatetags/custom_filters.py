from django import template

register = template.Library()

@register.filter(name='ownership')
def ownership(project, user):
	return project.added_by_user == user

@register.filter(name='ticket_owner')
def ownership(ticket, user):
    if ticket.user == user:
        return true;    
    return false

@register.filter(name='admin')
def adminship(project, user):
    if project.added_by_user == user:
        return true
    return false