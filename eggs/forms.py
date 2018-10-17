
from django import forms
from eggs.models import Reference, Sample
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

class ProcessSubmissionForm(forms.Form):
    #These next few lines grab the batch names used for use in the dropdown menu
    distinctBatchSamples = Sample.objects.distinct("batch").values()
    choiceSet=[]
    for specificSample in distinctBatchSamples:
        #2-tuples are required by django
        choice = (specificSample["batch"],specificSample["batch"])
        choiceSet.append(choice)
    #at the moment, this is done  without thought of the csv file. 
    batch_name = forms.ChoiceField(label="Enter the batch you wish to submit", choices=choiceSet)

#I wnoder if this will work for keeping some information the same against all
class SharedSampleForm(forms.Form):
    batch = forms.CharField(max_length=100)
