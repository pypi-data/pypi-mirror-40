from django.conf.urls import url

from bugtrack import views

urlpatterns = [
    url('^bug/$', views.bugs, name='bugs'),
    url('^bug/new/$', views.bug_new, name='bug_new'),
    url('^bug/(?P<bug_id>\d+)/$', views.bug, name='bug'),
    url('^bug/(?P<bug_id>\d+)/edit/$', views.bug_edit, name='bug_edit'),
]