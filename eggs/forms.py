
from django import forms
from eggs.models import Reference, Sample, Batch, Csv
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
        fields = ['batchName']

# This just gathers a Csv file before it is parsed.
class CsvForm(forms.ModelForm):
    class Meta: 
        model = Csv
        fields = ['csvFile']
    


