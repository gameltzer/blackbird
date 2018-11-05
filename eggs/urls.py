from django.conf.urls import url


from eggs import views
# this is for the static files

# from django.conf import settings
# from django.conf.urls.static import static 

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^uploadCSV',views.CSVView.as_view(), name = 'uploadCSV'),
    url(r'^uploadSelectFasta$',views.uploadSelectFasta, name ='uploadSelectFasta'),
    url(r'^uploadSelectFasta/uploadSample$',views.uploadSample, name ='uploadSample'),
    url(r'^submit$',views.submit, name ='submit'),
    # url(r'^submitCSV$', views.SubmitCSV.as_view(), name= 'SubmitCSV'),
    url(r'^graph$',views.graph, name='graph'),
    url(r'^tabulate$',views.tabulate, name='tabulate'),
    url(r'^graphCSV$',views.graphCSV, name='graphCSV'),
    url(r'^batchCreate$',views.batchCreate, name='batchCreate'),
    url(r'^)
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)