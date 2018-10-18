from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload$',views.upload, name ='upload'),
    url(r'^upload/uploadSample$',views.uploadSample, name ='uploadSample'),
    url(r'^submit$',views.submit, name ='submit'),
    url(r'^graph$',views.graph, name='graph'),
    url(r'^tabulate$',views.tabulate, name='tabulate'),
    url(r'^batchCreate$',views.batchCreate, name='batchCreate'),
]