# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadReferenceForm, UploadSampleForm, ProcessSubmissionForm
from django.forms import modelformset_factory
from eggs.models import Sample, Reference
from subprocess import call
import os 

# Create your views here.

from django.http import HttpResponse

def index(request):
    return render(request, 'eggs/index.html')

def upload(request):
    if request.method == 'POST':
        reference_form = UploadReferenceForm(request.POST, request.FILES)
        if reference_form.is_valid():
            reference_form.save()
            return HttpResponseRedirect('upload/uploadSample')
        else:
            context = {
                'reference_form' : reference_form
            }
    else:m
        context = {
            'reference_form' : UploadReferenceForm()
        }   
#    return render(request,'eggs/upload.html', context)
    return render(request,'eggs/upload.html', context)

def uploadSample(request):
    UploadSampleFormset = modelformset_factory(Sample, form = UploadSampleForm, extra=2)
    if request.method == 'POST':
        formset = UploadSampleFormset(request.POST, request.FILES)        
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('../submit')
        else:
            context = {
                'formset' : formset            }
    else:
        context = {
            'formset' : UploadSampleFormset(queryset=Sample.objects.none()) 
        }   
    return render(request,'eggs/uploadSample.html', context)

def submit(request):
    #this doesn't handle csv files
    if request.method =='POST':
        processForm = ProcessSubmissionForm(request.POST)
        if processForm.is_valid():
            batchSamples=Sample.objects.filter(batch__exact=request.POST['batch_name'])
         
    # the references should be the same for all, so we can just do the first reference of the sample. Might want to 
    # do checking later. 
            selectedReference = batchSamples[0].reference
    # This creates the arguments for the shell script
            sample1 =batchSamples[0].sampleFile
            sample2 =batchSamples[1].sampleFile
            reference = selectedReference.referenceFile
            fileBase= batchSamples[0].batch
    # This changes the directory to the one with the shell script (in the "aviary" media directory)        
            wd = os.getcwd()
            os.chdir("aviary")
    #This is the pipeline we use! 
            pipelineName="./nest.sh"
            call([pipelineName, sample1.name, sample2.name, reference.name, fileBase])
            os.chdir(wd)
            return HttpResponseRedirect('graph')
        else : 
            context = {
                'processForm' : processForm
            }
    else:
        context = {
        'processForm' : ProcessSubmissionForm()
        }
    return render(request,'eggs/submitSample.html', context)

def graph(request):
    return HttpResponse("This is the page for the graph")
