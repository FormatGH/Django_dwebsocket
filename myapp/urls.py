#!coding:utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^websocket$', views.websocket, name='websocket'),
    url(r'^testwebsocket$', views.testwebsocket, name='testwebsocket'),
    url(r'^start_task$', views.start_task, name='start_task'),
    url(r'^getprocess$', views.getprocess, name='getprocess'),
]