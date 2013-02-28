from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'labb2_project.views.home', name='home'),
    # url(r'^labb2_project/', include('labb2_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


    ##### projects
    url(r'^projects/$', 'project_app.views.project_list', name="project_list"),
    #url(r'^projects/add$', 'project_app.views.project_add', name="project_add"),
    #url(r'^project/(?P<project_id>\d+)/delete/$', 'project_app.views.project_delete', name="project_delete"),
    #url(r'^project/(?P<project_id>\d+)/edit/$', 'project_app.views.project_edit', name="project_edit"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
