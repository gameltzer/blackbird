
from django import forms
from eggs.models import Reference, Sample, Batch, CSV
# This is for uploading the reference file
class UploadReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ['referenceFile']

class UploadSampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        ## try handling batch and referenceFile in another form, possibly even another view
        fields =['sampleFile']


# Try maybe entering the batch on the reference page
class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['batchName','reference']

# This just gathers a CSV file before it is parsed.
class CSVForm(forms.ModelForm):
    class Meta: 
        model = CSV
        fields = ['csvFile']
