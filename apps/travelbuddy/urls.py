from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^profile/$', views.profile),
    url(r'^add_trip/$', views.add_trip),
    url(r'^process_trip/$', views.process_trip),
    url(r'^trip_details/(?P<id>\d+)?$', views.trip_details),
    url(r'^join_trip/(?P<id>\d+)$', views.join_trip),
]
