from django.conf.urls import url
from . import views
app_name = 'beltExam'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),
    url(r'^addScreen$', views.addScreen, name='addScreen'),
    url(r'^addTrip$', views.addTrip, name='addTrip'),
    url(r'^join/(?P<id>\d+)$', views.join, name='join')
]