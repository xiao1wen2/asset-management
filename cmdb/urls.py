"""ops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^idcs/(?P<pk>\d+)?/?$', IdcView.as_view(), name='idcs'),
    url(r'^api_idcs/(?P<pk>\d+)?/?$', APIIdcView.as_view(), name='api_idcs'),
    url(r'^racks/(?P<pk>\d+)?/?$', RackView.as_view(), name='racks'),
    url(r'^api_racks/(?P<pk>\d+)?/?$', APIRackView.as_view(), name='api_racks'),
    url(r'^servers/(?P<pk>\d+)?/?$', ServerView.as_view(), name='servers'),
    url(r'^api_servers/?(?P<pk>\d+)?/?$', APIServerView.as_view(), name='api_servers'),
    url(r'^dashboard/$', DashBoardView.as_view(), name='dashboard'),
    url(r'^api_dashboard/$', APIDashBoardView.as_view(), name='apidashboard'),
    url('^uploads/$', Insert_from_excel.as_view()),

]
