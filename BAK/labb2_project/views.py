from django.shortcuts import render_to_response, render, get_list_or_404
from labb2_project.models import Project_app

def home(request):
	test = "test"
	return render(request, 'test.html', {"test" : test})