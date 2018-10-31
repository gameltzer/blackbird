# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadReferenceForm, UploadSampleForm, BatchForm, CSVForm
from django.forms import modelformset_factory
from eggs.models import Sample, Reference, Batch,Result, CSV
from subprocess import call
import os 
from eggs.retrieveVcfData import *
from django.views import View

from django.core.files.uploadhandler import TemporaryFileUploadHandler

# Create your views here.

from django.http import HttpResponse

def index(request):
    return render(request, 'eggs/index.html')

# def chooseUpload(request):
#     return render(request, 'eggs/chooseUpload.html')

def uploadSelectFasta(request):
    if request.method == 'POST':
        reference_form = UploadReferenceForm(request.POST, request.FILES)
        if (reference_form.is_valid()):
            print(request.FILES)
            reference_form.save()
            return HttpResponseRedirect('batchCreate')
        else:
            context = {
                'reference_form' : reference_form,
            }
    else:
        # remove from the database the info
        refresh()
        context = {
            'reference_form' : UploadReferenceForm()
        }   
#    return render(request,'eggs/upload.html', context)
    return render(request,'eggs/uploadSelectFasta.html', context)

# def uploadCSV(request):
#     refresh()
#     return render(request, 'eggs/uploadCSV.html')

def batchCreate(request):
    if request.method == 'POST':
        batch_form = BatchForm(request.POST, request.FILES)
        if (batch_form.is_valid()):
            batch_form.save()
            return HttpResponseRedirect('uploadSelectFasta/uploadSample')
        else: 
            context = {
                'batch_form': batch_form
            }
    else:
        # remove from the database the info
       
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
    if request.method =='POST':
        result = Result.objects.latest("timeCreated")
        resultFileName = "final" + str(result.batch)+".vcf"
        wd = os.getcwd()
        # goes to the right directory
        os.chdir("aviary")
        #this function stores the vcfresults in the VCFRow Model
        storeVcf(resultFileName)
        # returns to previous directory
        os.chdir(wd)
        extractFromFormat(result)
        calculateVariants(result)
        exportToJson()
        return HttpResponseRedirect('graph')
    else:
        batch = Batch.objects.latest("timeCreated")
        result = Result(batch=batch)
        result.save()
        resultFileName = "final" + str(result.batch)+".vcf"
        context ={
        "resultFileName": resultFileName,
        }
    return render(request,'eggs/tabulate.html',context)

def graph(request):
    return render(request, 'eggs/graph.html')

# def tabulateCSV(request):
#     return render(request, 'eggs/tabulateCSV.html')

# This is the view for uploading a CSV. A class-based approach is used because
# it is much more complicated. 
class CSVView(View):
    form_class = CSVForm
    template_name = 'eggs/uploadCSV.html'
    # def success(self, request, template, filename):
    #     return HttpResponseRedirect('submitCSV')
  
    # this returns  a tuple with the id representing the CSV model object 
    # and the CSV lIST
    def handleUploadedFile(self, f):
        
        csvList =[]
        fileIter = iter(f)
        header = fileIter.next().rstrip().split(",")
        # the header should already be validated and cleaned
        # so that we know we have the result we want.  
        for line in fileIter:
            line = line.rstrip()
            #This creates a dictionary for each line, and then
            # puts it into a meat dictionary.
            lineCol= line.split(",")
            lineDict = {
                header[0]:lineCol[0],
                header[1]:lineCol[1],
                header[2]:lineCol[2],
            }
            csvList.append(lineDict)
        # for line in f:
        #     lineCols = line.split(",")
        c = CSV.objects.get(csvFile=f.name)
       
        # print (c.csvFile)

        csvTup=(c.csvFile, csvList)
        return csvTup
    
    # takes as an input a list represnting the contents of the CSV file and returns a 
    # data strucure with the different Reference objects (after creating the reference objects)
    # def getReferenceFiles(self, csvList):
    #     refList = []
    #     for row in csvList:
    #          ref = Reference(referenceFile=row['ReferenceFile'])
    #          ref.save()
    #          refList.append(ref)
    #     return refList

    # takes as input a list repythopresenting the contents of the csv file and the CSV entry
    def getDataFromCSV(self, csvTup):
        cName = csvTup[0]
        csvList = csvTup[1]
        # the earliest will be the one with all the references.

        csvObj = CSV.objects.filter(csvFile=cName).earliest("timeCreated")
        refList = []
        batchList = []
        
        for row in csvList:
            thisReference = row['ReferenceFile']
          #  fileObj = open(thisReference, "r")
           # fileDict = {thisReference: fileObj}
            
             #If we already have a file with tat name, we do not save.
            if not Reference.objects.filter(referenceFile=thisReference).exists():
                ref = Reference(referenceFile=thisReference)
                ref.save()
                refList.append(ref)
            thisBatchName = row['SampleName']
            if not Batch.objects.filter(batchName=thisBatchName).exists():
                thisReferenceObject = Reference.objects.get(referenceFile=thisReference)
                batch = Batch(csvID=csvObj, batchName=thisBatchName, reference=thisReferenceObject)
                batch.save()
                batchList.append(batch)
            # avoid redundant samples
            s = Sample(sampleFile=row['FastQFilename'],batch=Batch.objects.get(batchName=thisBatchName))
            s.save()
            # this might need to be cleaned up. 
        return csvObj

    def sendToPipeline(self, batchGroup):
        for batch in batchGroup:
            valueIter = batch.itervalues()
            keyIter = batch.iterkeys()
            valueList = valueIter.next()
            reference =str(Reference.objects.get(pk=valueList[0]).referenceFile.name)
            sample1 = str(valueList[1])
            sample2 = str(valueList[2])
            basename = str(keyIter.next())
            # This changes the directory to the one with the shell script (in the "aviary" media directory)        
            wd = os.getcwd()
            os.chdir("aviary")
    #This is the pipeline we use! 
            pipelineName="./nest.sh"
            call([pipelineName, sample1, sample2, reference, basename])
            os.chdir(wd)

    #This returns a list with the Result objects.
    def createResults(self, batchGroup):
        resList=[]
        for batch in batchGroup:
            keyIter = batch.iterkeys()
            basename = keyIter.next()
            # print(basename)
            res = Result(batch = Batch.objects.get(pk=basename))
            print(res)
            res.save()
            resList.append(res)
        return resList
 
    def storeVCFsFromCSV(self, resList):
        wd = os.getcwd()
        os.chdir("aviary")
        for res in resList:
            vcfName = "final"+ str(res.batch) +".vcf"
            storeVcf(vcfName)
            #Anything that doesn't have a result in it gets parsed and has a result.
            extractFromFormat(res)
            # these results are now parsed. 
            calculateVariants(res)

        os.chdir(wd)





    # this asks the user for a CSV file according to the CSVForm class. 
    def get(self,request):
        refresh()
        form = self.form_class()
        return render(request, self.template_name, {"form": form} )
    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            print(request.FILES) 
## try this!            
            form.save()
            csvFile = form.instance.csvFile
            print(csvFile)

            # csvPath = form.fields["csvFile"]
            # csvFile = request.FILES['csvFile']
            # print("path" + csvPath.name)
            # print("file:" + str(type(csvFile)))
            # print("path:" + csvFile.temporary_file_path())

            csvList = self.handleUploadedFile(csvFile)
          
            # refList = self.getReferenceFiles(c(svList)
            csvStore = self.getDataFromCSV(csvList)
            # print(form['csvFileName'].data)
            batches = csvStore.batch_set.all()
            # print(batches)
            csvBatchDictList = []
            for batch in batches:
                # print(batch)
                samples = batch.sample_set.all()
                # print(samples.count())
                sampleList = []
                for sample in samples:
                    # print(sample)
                    sampleList.append(sample)
                batchDict ={batch.batchName: [ batch.reference_id, samples[0], samples[1]] }
                csvBatchDictList.append(batchDict)
            print(csvBatchDictList)
            self.sendToPipeline(csvBatchDictList)
            resList = self.createResults(csvBatchDictList)
            self.storeVCFsFromCSV(resList)
            exportToJson()
            return HttpResponseRedirect('graphCSV')
        return render(request, self.template_name, {"form":form})

# class SubmitCSV(View):
#     def get(self,request):
#     def post(self,request):
#     #this doesn't handle csv files. 
#     # also consider creating 
#     #
#     # The arguments for the shell script
#     batch=Batch.objects.latest("timeCreated")
#     reference=batch.reference
#     samples = []
#     # this gets the associated samples
#     for sample in batch.sample_set.all():
#         samples.append(sample)
#     sample1 = samples[0]
#     sample2 = samples[1]
#     context = {
#             "batch" : batch,
#             "reference" : reference,
#             "sample1" : sample1,
#             "sample2" : sample2,
#         }
#     if request.method =='POST':
#             #The batch we are working with. 
#     # This changes the directory to the one with the shell script (in the "aviary" media directory)        
#             wd = os.getcwd()
#             os.chdir("aviary")
#     #This is the pipeline we use! 
#             pipelineName="./nest.sh"
#             call([pipelineName, sample1.sampleFile.name, sample2.sampleFile.name, reference.referenceFile.name, batch.batchName])
#             os.chdir(wd)
#             return HttpResponseRedirect('tabulate')
#     return render(request, "eggs/submitCSV.html")

def graphCSV(request):
    return render(request, 'eggs/graphCSV.html')