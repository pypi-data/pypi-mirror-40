from django.conf.urls import url


urlpatterns = [
    url('^/bug/$', views.bug, name='bug'),
]