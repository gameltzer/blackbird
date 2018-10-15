# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadReferenceForm, UploadSampleForm
from django.forms import modelformset_factory
from eggs.models import Sample

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
    else:
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
    return HttpResponse("this is the page for submitting")

def graph(request):
    return HttpResponse("This is the page for the graph")