from django.conf.urls import url


from eggs import views
# this is for the static files

from blackbird import settings
from django.conf.urls.static import static 

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^uploadCsv',views.CsvView.as_view(), name = 'uploadCsv'),
    url(r'uploadSingleBatch', views.UploadSingleBatch.as_view(), name="uploadSingleBatch"),
    # url(r'^uploadSelectFasta$',views.uploadSelectFasta, name ='uploadSelectFasta'),
    # url(r'^uploadSelectFasta/uploadSample$',views.uploadSample, name ='uploadSample'),
    url(r'^submit$',views.submitSingle, name ='submit'),
    url(r'^submitCsv$', views.SubmitCsv.as_view(), name= 'submitCsv'),
    url(r'^graph$',views.graph, name='graph'),
    # url(r'^tabulate$',views.tabulate, name='tabulate'),
    url(r'^graphCsv$',views.graphCsv, name='graphCsv'),
    # url(r'^batchCreate$',views.batchCreate, name='batchCreate'),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)