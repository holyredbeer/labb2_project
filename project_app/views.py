from django.shortcuts import get_list_or_404, render
from project_app.models import Project

def project_list(request):
	projects = get_list_or_404(Project.objects.order_by('name'))
	return render(request, 'projects/list.html', {"projects" : projects})