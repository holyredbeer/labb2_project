from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^labb2_project/', include('labb2_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', 'project_app.views.home', name="home"),

    ##### login:
    url(r'^login/$', 'project_app.views.login_user', name='login'),
    url(r'^logout/$', 'project_app.views.logout_user', name='logout'),
    #url(r'^permission/error/$', 'project_app.views.error_permission', name='error_permission'),

    ##### projects
    url(r'^projects/filter/(?P<projects_to_show>\w+)$', 'project_app.views.project_list_filtered', name="project_list_filtered"),
    url(r'^projects/$', 'project_app.views.project_list', name="project_list"),
    url(r'^project/$', 'project_app.views.goto_projects', name="goto_projects"),
    url(r'^projects/(?P<project_id>\d+)/$', 'project_app.views.show_project', name="show_project"),
    url(r'^projects/add$', 'project_app.views.project_add', name="project_add"),
    url(r'^projects/manage$', 'project_app.views.project_manage', name="project_manage"),
    url(r'^tickets/$', 'project_app.views.users_tickets', name="users_tickets"),
    url(r'^project/(?P<project_id>\d+)/delete/$', 'project_app.views.project_delete', name="project_delete"),
    url(r'^project/(?P<project_id>\d+)/edit/$', 'project_app.views.project_edit', name="project_edit"),
    #url(r'^projects/user/(?P<user_id>\d+)/$', 'project_app.views.projects_for_user', name="projects_for_user"),
    
    ##### tickets
    url(r'^project/(?P<project_id>\d+)/ticket/add$', 'project_app.views.ticket_add', name="ticket_add"),
    url(r'^project/(?P<project_id>\d+)/ticket/(?P<ticket_id>\d+)/$', 'project_app.views.show_ticket', name="show_ticket"),
    url(r'^ticket/(?P<ticket_id>\d+)/delete/$', 'project_app.views.ticket_delete', name="ticket_delete"),
    url(r'^project/(?P<project_id>\d+)/ticket/(?P<ticket_id>\d+)/edit/$', 'project_app.views.ticket_edit', name="ticket_edit"),

    #url(r'^project/(?P<project_id>\d+)/tickets/$', 'project_app.views.ticket_list', name="ticket_list"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
