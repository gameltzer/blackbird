# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import os
# import threading
import time
from subprocess import Popen, call, check_output

from django.core.files import File
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import StreamingHttpResponse
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.views import View
import threading
from eggs.models import Batch, Csv, Reference, Result, Sample
from eggs.retrieveVcfData import (calculateVariants, exportToJson,
                                  extractFromFormat, refresh, saveFileField,
                                  storeVcf)

from .forms import BatchForm, CsvForm, UploadReferenceForm, UploadSampleForm

# from .tasks import celery_extractDataFromCsv, add, testModel
# from blackbird.celery import debug_task
# from django.db import transaction
#This is for the log. 

logger = logging.getLogger("django.server")

# Create your views here.




def index(request):
    #Session expires when browser closes. 
    request.session.set_expiry(0)
 
    return render(request, 'eggs/index.html')

# def chooseUpload(request):
#     return render(request, 'eggs/chooseUpload.html')
class UploadSingleBatch(View):
    template_name = 'eggs/uploadSingleBatch.html'
    reference_form_class = UploadReferenceForm
    batch_form_class = BatchForm
    UploadSampleFormset = modelformset_factory(Sample, form = UploadSampleForm, extra=2)
    def get(self, request):
        refresh()
        reference_form = self.reference_form_class()
        batch_form = self.batch_form_class()
       
        formset = self.UploadSampleFormset(queryset=Sample.objects.none())
        logger.info(reference_form)
        return render(request, self.template_name, {"reference_form": reference_form, "batch_form": batch_form, "formset": formset} )

    def post(self,request):
        reference_form = self.reference_form_class(request.POST, request.FILES)
        batch_form = self.batch_form_class(request.POST)
        logger.info(batch_form)
        if reference_form.is_valid():
            logger.info("reference form valid")
            logger.info(request.FILES)            
            reference_form.save()
            reference_Obj = reference_form.instance
            logger.info(reference_Obj)
           
            if batch_form.is_valid():
                batch_Obj = batch_form.instance
                batch_Obj.reference = reference_Obj
                batch_Obj.save()
                logger.info(batch_Obj)
                logger.info(batch_Obj.reference)
                formset = self.UploadSampleFormset(request.POST, request.FILES)        
                if formset.is_valid():
# The sampes should be saved when addedd
                    for form in formset:
                        batch_Obj.sample_set.add(form.instance, bulk=False)
                    formset.save()

                    logger.info(batch_Obj)
                    # logger.info(batch_Obj.sample_set.all())
                else:
                    raise Exception
            else: 
                raise Exception
        else:
            raise Exception
        request.session["batchName"] = batch_Obj.batchName
#Try saving the primary key instead.
        return HttpResponseRedirect("submit")
    


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

# this is the Get processing for tabulating the VCF

def tabulateGet(batch):
    resultQuerySet=Result.objects.filter(batch=batch.batchName)
    logger.info(batch)
    logger.info(resultQuerySet)
  

    # # Prevents entering duplicates, which isn't allowed by the relation *result*.
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
    logger.info("ResultBatch and result File at the end of GET proessing:\n " + str(result.batch) +", "+ resultFileName)
    return resultFileName

#This is the post processing for tabulating the VCF
def tabulatePost(batch, resultFileName):
    logger.info("post")
    result = Result.objects.get(batch=batch.batchName)
    resultQuery = Result.objects.filter(batch=result.batch)
    # resultFileName = "final" + str(result.batch)+".vcf"
    wd = os.getcwd()
    # goes to the right directory
    if not wd.endswith("/aviary"):
        os.chdir("aviary")
    #this function stores the vcfresults in the VCFRow Model
    storeVcf(resultFileName)
    # returns to previous directory
    os.chdir(wd)
    logger.info(result)
    extractFromFormat(result)
    calculateVariants(result)
    exportToJson(resultQuery)

   

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
    resultFileName=tabulateGet(batch)
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
        tabulatePost(batch, resultFileName)
        #A redirect is not returned because the redirect needs to be handled with JavaScript to make sure that django doesn't "step over" the ajax being used for the loader and conflict with it.
        return  HttpResponse("Done.")
    return render(request,'eggs/submitSample.html', context)

def tabulate(request):
    # The batch object is retrieved using the information in the setting.
    thisBatch = Batch.objects.get(batchName=request.session["batchName"])
    tabulateGet(thisBatch)
    resultFileName = "final" + str(thisBatch)+".vcf"
    
        
    # print("this is the result: " + str(result))
    if request.method =='POST':
        tabulatePost(thisBatch,resultFileName)
        
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
    # This is so we know when we are done extracting to signla to the thread. 
    doneExtracting = threading.Event()
    

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
        thisFilename = f.name
        if Csv.objects.filter(csvFile=thisFilename).exists():
            c= Csv.objects.get(csvFile=thisFilename)
        else: 
            c = Csv(csvFile=thisFilename)
            c.save()
       
        logger.info("CSV information: csvID {csvID} ".format(csvID=c.pk, csvFile=c.csvFile))

        csvTup=(c.pk, csvList)
        logger.info("Tup 1 type{0}:".format(str(type(csvTup[0]))))

        return csvTup
    
    # takes as an input a list represnting the contents of the Csv file and returns a 
    # data strucure with the different Reference objects (after creating the reference objects)
    # def getReferenceFiles(self, csvList):
    #     refList = []
    #     for row in csvList:
    #          ref = Reference(referenceFile=row['ReferenceFile'])
    #          ref.save()
    #          refList.append(ref)
    #     return refList

# Takes as input a a tuple representing the contents of the Csv file and the Csv file itself.
# It then parses the file and saves the contents to a relevant model object so that it goes in the database. 
    def extractDataFromCsv(self, csvTup):
        logger.info("getDataFromCsv reached")
        csvObj = Csv.objects.get(pk=csvTup[0])
        # cName = csvObj.csvFile
        csvList = csvTup[1]


      
        refList = []
        batchList = []
        progressDot = ""
        for row in csvList:
            progressDot +="." 
            # yield progressDot
            # yield "Procesing."
            thisReference = row['ReferenceFile']
          #  fileObj = open(thisReference, "r")
           # fileDict = {thisReference: fileObj}
            
#If we already have a file with that name, we do not save.
            if not Reference.objects.filter(referenceFile=thisReference).exists():
                ref = Reference(referenceFile=thisReference)
                ref.save()
                logger.info("reference:" + str(ref.referenceFile))
                newReferenceFileName= saveFileField(ref.referenceFile)
                # this updates the filename to the new location.
                logger.info("Type: "+ str(type(ref.referenceFile)))
                ref.referenceFile= newReferenceFileName
                logger.info("NewReferenceFilename:" + str(ref.referenceFile))
                ref.save()
                thisReference=ref.referenceFile
            
                refList.append(ref)
            thisBatchName = row['SampleName']
            if not Batch.objects.filter(batchName=thisBatchName).exists():
                thisReferenceObject = Reference.objects.get(referenceFile=thisReference)
                batch = Batch(csvID=csvObj, batchName=thisBatchName, reference=thisReferenceObject)
                batch.save()
                batchList.append(batch)
            # avoid redundant samples
            logger.info(row['FastQFilename'])
            # The batch should exist by now. 
       
            thisBatch=Batch.objects.get(batchName=thisBatchName)
            s = Sample(sampleFile=row['FastQFilename'],batch=thisBatch)
            s.save()
            logger.info("Sample {sample}, {batch}".format(sample=s.pk,batch=str(s.batch)))
            newSampleFileName = saveFileField(s.sampleFile)
            s.sampleFile=newSampleFileName
            logger.info("NewSampleFilename:" + str(s.sampleFile))
            s.save()
            
        # This sends a signal to the event object for stopping waiting.  
        self.doneExtracting.set()

  

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
        body = str(request.path)
        logger.info("Request: " + body)
        # if (body == "Done?"):    
        #     return HttpResponse("No.")
        # else:
        # refresh()
        form = self.form_class()
        logger.info(form)
        return render(request, self.template_name, {"form": form} )

#     def post(self,request):
#         logger.info("post for Csv reached")
#         form = self.form_class(request.POST, request.FILES)
#         logger.info("contents of bound form: \n"+ str(request.POST))
#         logger.info("files of bound form: \n" + str(request.FILES))
#         logger.info("before validation" + str(form))
#         # logger.info(request.body)
       
#         if form.is_valid():
#             logger.info("form valid")
#             logger.info(request.FILES)            
#             form.save()
#             csvFile = form.instance.csvFile
#             thisCsv = Csv.objects.get(csvFile=csvFile)
#             logger.info(thisCsv)
# #Try saving the primary key instead.
#             request.session["csvFile"]=thisCsv.id
#         else:
#             logger.info("form invalid")
#             logger.info(form)
#             raise Exception
        
    def post(self,request):
        logger.info("post for Csv reached")
        form = self.form_class(request.POST, request.FILES)
        logger.info("contents of bound form: \n"+ str(request.POST))
        logger.info("files of bound form: \n" + str(request.FILES))
        logger.info("before validation" + str(form))
        # logger.info(request.body)
       
        if form.is_valid():
            logger.info("form valid")
            logger.info(request.FILES)            
            form.save()
            thisCsv = form.instance
            csvFile = thisCsv.csvFile
            # thisCsv = Csv.objects.get(csvFile=csvFile)
            logger.info(thisCsv)
#Try saving the primary key instead.
            request.session["csvFile"]=thisCsv.id
            csvTup = self.handleUploadedFile(csvFile)
            # self.extractDataFromCsv(csvTup)
            logger.info("csvTup  {0};".format(csvTup))
            logger.info("csvRetrieved {0}".format(thisCsv.id))
            # # testModel.delay(csvTup[0])
            # # celery_extractDataFromCsv.delay(csvTup)
            # # debug_task.delay()
            # logger.info("Celery extraction reached")
            # # this is the thread. 
            # thread = threading.Thread(target = self.extractDataFromCsv(csvTup))
            # # thread.daemon= True 
            # thread.start()
            # # self.extractDataFromCsv(csvTup)
            # # This causes it to wait
            # self.doneExtracting.wait()
            # # This will be encoded into JSON that will be sent to ajax so that ajax can send the window to another URL. AJAX doesn't understand the 
            # # HTTP redirects in Django. 
            # response = {'status': 1,'url':'submitCsv'}
            #The redirect is handled in the javascript. 
            
            self.extractDataFromCsv(csvTup)
            # return HttpRespons("Done")
            # return StreamingHttpResponse(self.extractDataFromCsv(csvTup),content_type="text/html; charset=utf-8")
            # return HttpResponse(json.dumps(response), content_type="application/json")
            return HttpResponseRedirect("submitCsv")
        else:
            logger.info("form invalid")
            logger.info(form)
            raise Exception
           
        return render(request, self.template_name, {"form":form})

class SubmitCsv(View):
    template_name = 'eggs/submitCsv.html'
    csvBatchDictList = []
    def sendToPipeline(self, batchGroup):
        for batch in batchGroup:
            valueIter = batch.itervalues()
            keyIter = batch.iterkeys()
            valueList = valueIter.next()
            logger.info("valueList 0 (refererence):{0}".format(valueList[0]))
            # referenceName = Reference.objects.get(pk=valueList[0]).referenceFile.name
            referenceName=valueList[0]
            logger.info("Reference name{0}".format(referenceName))
            # reference =str(Reference.objects.get(pk=valueList[0]).referenceFile.name)
            reference =str(referenceName)

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
    def get(self,request):
        csvID = request.session["csvFile"]
        logger.info(csvID)
        logger.info(str(Csv.objects.all()))
        thisCSV= Csv.objects.get(pk=csvID)
#This gets the associated batches that have been extracted from the CSV file.
        batches = thisCSV.batch_set.all()
        logger.info("\tThe batches for the class-based view 'SubmitCSV' are: \n {0}".format(str(batches.values())))
        allBatches=Batch.objects.all().values()
        logger.info("\n\t All the batches in the dataase are: \n {0}".format(str(allBatches)))
        
        for batch in batches:
            logger.info("BatcH: {batch}".format(batch=str(batch)))
            samples = batch.sample_set.all()
            logger.info("content Batch: {batch}".format(batch=str(batch)))
            # sampleList = []
            # for sample in samples:
            #     sampleList.append(sample)
            batchDict ={batch.batchName: [ batch.reference, samples[0], samples[1]] }
            self.csvBatchDictList.append(batchDict)
        # print(CsvBatchDictList)
        # self.sendToPipeline(CsvBatchDictList)
            # resList = self.createResults(CsvBatchDictList)
            # self.storeVCFsFromCsv(resList)
            # exportToJson(resList)
        csvContents = ""
        for element in self.csvBatchDictList:
            logger.info("Element: {element}".format(element=str(element)))
            elementItems=element.items()
            key, values= elementItems[0]
            batchName = str(key)
            reference = str(values[0])
            sample1 = str(values[1])
            sample2 = str(values[2])
            logger.info("element")
            csvContents += "The batch {batchName} has as a reference file {reference}, \n   and as sample files {sample1} \n    and {sample2}. \n\n ".format(batchName=batchName,
            reference=reference,sample1=sample1,sample2=sample2)
        logger.info("CSV contents {csvContents}".format(csvContents=csvContents))
        logger.info("CSV file {csvFile}".format(csvFile=str(thisCSV.csvFile)))
        context={
            "csvFile": thisCSV.csvFile,
            "fileContents": csvContents
            }
        response = TemplateResponse(request, self.template_name, context=context)
        logger.info("This was attempted with the template response.")
        return response
    def post(self,request):
        postMessage = "POST \n"
        postFile = open("postLog","a")
        postFile.write(postMessage)
        postFile.flush()
        os.fsync(postFile)
        self.sendToPipeline(self.csvBatchDictList)
    #this doesn't handle Csv files. 
    # also consider creating 
    #
    # # The arguments for the shell script
    #     batch=Batch.objects.latest("timeCreated")
    #     reference=batch.reference
    #     samples = []
    #     # this gets the associated samples
    #     for sample in batch.sample_set.all():
    #         samples.append(sample)
    #     sample1 = samples[0]
    #     sample2 = samples[1]
    #     # context = {
    #     #         "batch" : batch,
    #     #         "reference" : reference,
    #     #         "sample1" : sample1,
    #     #         "sample2" : sample2,
    #     #     }
    # #     if request.method =='POST':
    #             #The batch we are working with. 
    #     # This changes the directory to the one with the shell script (in the "aviary" media directory)        
    #     wd = os.getcwd()
    #     os.chdir("aviary")
    #     #This is the pipeline we use! 
    #     pipelineName="./nest.sh"
    #     call([pipelineName, sample1.sampleFile.name, sample2.sampleFile.name, reference.referenceFile.name, batch.batchName])
    #     os.chdir(wd)
        # The redirect is handled in the javascript. 

        response = {'status': 1,'url':'graphCsv'}
        return HttpResponse(json.dumps(response), content_type="application/json")
        # return HttpResponseRedirect('graphCsv')

def graphCsv(request):
    return render(request, 'eggs/graphCsv.html')
