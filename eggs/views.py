# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UploadReferenceForm, UploadSampleForm, BatchForm, CsvForm
from django.forms import modelformset_factory
from eggs.models import Sample, Reference, Batch,Result, Csv
from subprocess import call, check_output,Popen
import os 
from eggs.retrieveVcfData import *
from django.views import View
import logging
from django.core.files.uploadhandler import TemporaryFileUploadHandler

#This is for the log. 

logger = logging.getLogger("django.server")

# Create your views here.

from django.http import HttpResponse

def index(request):
    #Session expires when browser closes. 
    request.session.set_expiry(0)
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

# def uploadCsv(request):
#     refresh()
#     return render(request, 'eggs/uploadCsv.html')

def batchCreate(request):
    if request.method == 'POST':
        batch_form = BatchForm(request.POST, request.FILES)
        if (batch_form.is_valid()):
            batch_form.save()
# this stores the batch name we have retrieved
            request.session["batchName"] = batch_form.instance.batchName
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
    #The batch object is retrieved using the name in the session.
    thisBatch = Batch.objects.get(batchName=request.session["batchName"])
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
            # return HttpResponseRedirect("bozo")
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
    #this doesn't handle Csv files. 
    # also consider creating 
    #
    # The arguments for the shell script
    # The batch object is retrieved using the information in the session. 
    batch=Batch.objects.get(batchName=request.session["batchName"])
    # print(batch.batchName)
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
    if request.method =='POST' :
          
        #The batch we are working with. 
# This changes the directory to the one with the shell script (in the "aviary" media directory)        
        wd = os.getcwd()
        if not wd.endswith("/aviary"):
            os.chdir("aviary")
#This is the pipeline we use! 
        pipelineName="./nest.sh"
        # f = file("log", "w")
        pipe = Popen([pipelineName, sample1.sampleFile.name, sample2.sampleFile.name, reference.referenceFile.name, batch.batchName])
        pipe.wait()
        os.chdir(wd)
        print(os.getcwd())
        #A redirect is not returned because the redirect needs to be handled with JavaScript to make sure that django doesn't "step over" the ajax being used for the loader and conflict with it.
        return  HttpResponse("Done.")
    return render(request,'eggs/submitSample.html', context)

def tabulate(request):
    # The batch object is retrieved using the information in the setting.
    batch = Batch.objects.get(batchName=request.session["batchName"])
    resultQuerySet=Result.objects.filter(batch=batch.batchName)
    logger.info(batch)
    logger.info(resultQuerySet)
  

    # Prevents enteriing duplicates, which isn't allowed by the relation *result*.
    if resultQuerySet.exists():
        logger.info("condition1")
        result = Result.objects.get(batch=batch)
        logger.info(result.batch)

    else: 
        logger.info("condition2")
        # the problem has something to do wit this#
        result = Result(batch=batch)
        # logger.info(Result.objects.get(batch=batch.batchName).batch)
        logger.info("Before save: " + str(result.batch))
        logger.info("batches:" + str(Batch.objects.all()))
        result.save()
    resultFileName = "final" + str(result.batch)+".vcf"
    logger.info("After save: " + str(result.batch))
        
    print("this is the result: " + str(result))
    if request.method =='POST':
        logger.info("post")
        result = Result.objects.get(batch=request.session["batchName"])
        resultQuery = Result.objects.filter(batch=result.batch)
        resultFileName = "final" + str(result.batch)+".vcf"
        wd = os.getcwd()
        # goes to the right directory
        if not wd.endswith("/aviary"):
            os.chdir("aviary")
        #this function stores the vcfresults in the VCFRow Model
        storeVcf(resultFileName)
        # returns to previous directory
        os.chdir(wd)
        extractFromFormat(result)
        calculateVariants(result)
        exportToJson(resultQuery)
        return HttpResponseRedirect('graph')
    context ={
    "resultFileName": resultFileName,
    }  
    print(resultFileName)
    return render(request,'eggs/tabulate.html', context)

def graph(request):
    return render(request, 'eggs/graph.html')

# def tabulateCsv(request):
#     return render(request, 'eggs/tabulateCsv.html')

# This is the view for uploading a Csv. A class-based approach is used because
# it is much more complicated. 
class CsvView(View):
    form_class = CsvForm
    template_name = 'eggs/uploadCsv.html'
    # def success(self, request, template, filename):
    #     return HttpResponseRedirect('submitCsv')
  
    # this returns  a tuple with the id representing the Csv model object 
    # and the Csv lIST
    def handleUploadedFile(self, f):
        logger.info("handleUploadedFile reached")
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
        c = Csv.objects.get(csvFile=f.name)
       
        # print (c.CsvFile)

        CsvTup=(c.csvFile, csvList)
        return CsvTup
    
    # takes as an input a list represnting the contents of the Csv file and returns a 
    # data strucure with the different Reference objects (after creating the reference objects)
    # def getReferenceFiles(self, csvList):
    #     refList = []
    #     for row in csvList:
    #          ref = Reference(referenceFile=row['ReferenceFile'])
    #          ref.save()
    #          refList.append(ref)
    #     return refList

    # takes as input a list repythopresenting the contents of the Csv file and the Csv entry
    def getDataFromCsv(self, csvTup):
        logger.info("getDataFromCsv reached")
        cName = csvTup[0]
        csvList = csvTup[1]
        # the earliest will be the one with all the references.

        csvObj = Csv.objects.filter(csvFile=cName).earliest("timeCreated")
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
            if not wd.endswith("/aviary"):
                os.chdir("aviary")  
    #This is the pipeline we use! 
            pipelineName="./nest.sh"
            call([pipelineName, sample1, sample2, reference, basename])
            logger.info("pipeline called")
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
 
    def storeVCFsFromCsv(self, resList):
        wd = os.getcwd()
        if not wd.endswith("/aviary"):
            os.chdir("aviary")
        for res in resList:
            vcfName = "final"+ str(res.batch) +".vcf"
            storeVcf(vcfName)
            #Anything that doesn't have a result in it gets parsed and has a result.
            extractFromFormat(res)
            # these results are now parsed. 
            calculateVariants(res)

        os.chdir(wd)

    # this asks the user for a Csv file according to the CsvForm class. 
    def get(self,request):
        logger.info("get for Csv reached")

        # refresh()
        form = self.form_class()
        logger.info(form)
        return render(request, self.template_name, {"form": form} )

    def post(self,request):
        logger.info("post for Csv reached")
        form = self.form_class(request.POST, request.FILES)
        logger.info("contents of bound form: \n"+ str(request.POST))
        logger.info("files of bound form: \n" + str(request.FILES))
        logger.info("before validation" + str(form))
        if form.is_valid():
            logger.info("form valid")
            logger.info(request.FILES)            
            form.save()
            csvFile = form.instance.csvFile
            request.session["csvFile"]=csvFile
            logger.info(csvFile)


            csvList = self.handleUploadedFile(csvFile)
          
            csvStore = self.getDataFromCsv(csvList)
            # store the data in the session. 
            request.session["csvStore"]=csvStore
            """Move to next view"""
            # batches = CsvStore.batch_set.all()
            # CsvBatchDictList = []
            # for batch in batches:
            #     samples = batch.sample_set.all()
            #     sampleList = []
            #     for sample in samples:
            #         sampleList.append(sample)
            #     batchDict ={batch.batchName: [ batch.reference_id, samples[0], samples[1]] }
            #     CsvBatchDictList.append(batchDict)
            # print(CsvBatchDictList)
            # self.sendToPipeline(CsvBatchDictList)
            # resList = self.createResults(CsvBatchDictList)
            # self.storeVCFsFromCsv(resList)
            # exportToJson(resList)
            return HttpResponseRedirect('submitCsv')
        else:
            logger.info("form invalid")
            logger.info(form)
           
        return render(request, self.template_name, {"form":form})

class SubmitCsv(View):
    template_name = 'eggs/submitCsv.html'
    def get(self,request):
        context={"csvFile": request.session["csvFile"],}
        return render(request, self.template_name, context)
    def post(self,request):
    #this doesn't handle Csv files. 
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
                return HttpResponseRedirect('graphCsv')

def graphCsv(request):
    return render(request, 'eggs/graphCsv.html')