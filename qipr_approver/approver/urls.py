from django.conf.urls import url
from django.contrib.auth.views import logout
from approver import views, api

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^shib/$', views.fake_shib, name='shib'),
    url(r'^projects/$', views.project, name='projects'),
    url(r'^projects/similar/(?P<project_id>[0-9]+)/$', views.similar_projects, name='similar_projects'),
    url(r'^projects/(?P<project_id>[0-9]+)/$', views.project, name='projects'),
    url(r'^approver/$', views.approve, name='approve'),
    url(r'^approver/(?P<project_id>[0-9]+)/$', views.approve, name='approve'),
    url(r'^project_status/$', views.project_status, name='project_status'),
    url(r'^project_status/(?P<project_id>[0-9]+)/$', views.project_status, name='project_status'),
    url(r'^aboutyou/$', views.about_you, name='aboutyou'),
    url(r'^answer_submit/$', api.answer_submit, name='answer_submit'),
    url(r'^first_login/$', views.first_login, name='firstlogin'),
    url(r'^dashboard/(?P<project_id>[0-9]+)$', views.dashboard, name='project_del'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^api/$', api.index, name='api_index'),
    url(r'^api/users$', api.users, name='api_users'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
]
