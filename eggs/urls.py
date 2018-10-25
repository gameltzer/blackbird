from django.conf.urls import url


from . import views
# this is for the static files

# from django.conf import settings
# from django.conf.urls.static import static 

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload$',views.upload, name ='upload'),
    url(r'^upload/uploadSample$',views.uploadSample, name ='uploadSample'),
    url(r'^submit$',views.submit, name ='submit'),
    url(r'^graph$',views.graph, name='graph'),
    url(r'^tabulate$',views.tabulate, name='tabulate'),
    url(r'^batchCreate$',views.batchCreate, name='batchCreate'),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)