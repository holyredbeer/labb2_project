from django import template

register = template.Library()

### Projects
@register.filter(name='ownership')
def ownership(project, user):
	return project.added_by_user == user

@register.filter(name='membership')
def membership(project, user):
	return project.users.filter(id=user.id).exists()


### Tickets
@register.filter(name='ticket_owner')
def ownership(ticket, user):
	return ticket.user == user

### Ta bort?
@register.filter(name='admin')
def adminship(project, user):
    if project.added_by_user == user:
        return true
    return false