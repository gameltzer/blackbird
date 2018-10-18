# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from django.forms import modelformset_factory
from eggs.models import Sample, Reference, Batch
from subprocess import call
import os 

# Create your views here.

from django.http import HttpResponse

def index(request):
    return render(request, 'eggs/index.html')

def upload(request):
    if request.method == 'POST':
        reference_form = UploadReferenceForm(request.POST, request.FILES)
        if (reference_form.is_valid()):
            reference_form.save()
            return HttpResponseRedirect('batchCreate')
        else:
            context = {
                'reference_form' : reference_form,
            }
    else:
        context = {
            'reference_form' : UploadReferenceForm()
        }   
#    return render(request,'eggs/upload.html', context)
    return render(request,'eggs/upload.html', context)

def batchCreate(request):
    if request.method == 'POST':
        batch_form = BatchForm(request.POST, request.FILES)
        if (batch_form.is_valid()):
            batch_form.save()
            return HttpResponseRedirect('upload/uploadSample')
        else: 
            context = {
                'batch_form': batch_form
            }
    else:
        context = { 
            'batch_form' : BatchForm()
        }
    return render(request, "eggs/createBatch.html",context)


def uploadSample(request):
    UploadSampleFormset = modelformset_factory(Sample, form = UploadSampleForm, extra=2)
    thisBatch = Batch.objects.latest('timeCreated')
    batchName = thisBatch.batchName
    batchReference = thisBatch.reference
    if request.method == 'POST':
        formset = UploadSampleFormset(request.POST, request.FILES)        
        if formset.is_valid():
# The idea is to auto-populate this with the batch 
# created in the last step. (it should be the latest one created,
# we aren't worried about multiple users).
# This also means I don't need to worry about the reference,
#  because it's part of the batch.
            for form in formset:
                thisBatch.sample_set.add(form.instance, bulk=False)
            formset.save()
            return HttpResponseRedirect('../submit')
        else:
            context = {
                'formset' : formset, 
                'nameOfBatch' : batchName,
                'associatedReference' : batchReference,

            }
    else:
        context = {
            'formset' : UploadSampleFormset(queryset=Sample.objects.none()) ,
            'nameOfBatch' : batchName,
            'associatedReference' : batchReference,

        }   
    return render(request,'eggs/uploadSample.html', context)

def submit(request):
    #this doesn't handle csv files. 
    # also consider creating 
    #
    # The arguments for the shell script
    batch=Batch.objects.latest("timeCreated")
    reference=batch.reference
    samples = []
    # this gets the associated samples
    for sample in batch.sample_set.all():
        samples.append(sample)
    sample1 = samples[0]
    sample2 = samples[1]
    context = {
            "batch" : batch,
            "reference" : reference,
            "sample1" : sample1,
            "sample2" : sample2,
        }
    if request.method =='POST':
            #The batch we are working with. 
    # This changes the directory to the one with the shell script (in the "aviary" media directory)        
            wd = os.getcwd()
            os.chdir("aviary")
    #This is the pipeline we use! 
            pipelineName="./nest.sh"
            call([pipelineName, sample1.sampleFile.name, sample2.sampleFile.name, reference.referenceFile.name, batch.batchName])
            os.chdir(wd)
            return HttpResponseRedirect('tabulate')
    return render(request,'eggs/submitSample.html', context)

def tabulate(request):
    return render(request,'eggs/tabulate.html')

def graph(request):
    return HttpResponse("This is the page for the graph")
