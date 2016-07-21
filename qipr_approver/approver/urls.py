from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views, api

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^shib/$', views.fake_shib, name='shib'),
    url(r'^projects/$', views.project, name='projects'),
    url(r'^aboutyou/$', views.about_you, name='aboutyou'),
    url(r'^first_login/$', views.first_login, name='firstlogin'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^api/$', api.index, name='api_index'),
    url(r'^api/users$', api.users, name='api_users'),
    url(r'^logout/$', logout, {'next_page': '/shib'}, name='logout'),
]
