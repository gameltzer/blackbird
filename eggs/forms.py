from django.forms import ModelForm
from eggs.models import Reference, Sample
# This is for uploading the reference file
class UploadReferenceForm(ModelForm):
    class Meta:
        model = Reference
        fields = ['referenceFile']

class UploadSampleForm(ModelForm):
    class Meta:
        model = Sample
        fields =['batch','sampleFile','reference']
