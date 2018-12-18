from __future__ import absolute_import, unicode_literals
from celery import shared_task
import logging
from .models import Csv, Reference,Batch, Sample
from .retrieveVcfData import saveFileField
# from .views import saveFileField
logger = logging.getLogger("django.server")
# # This is a function version of the saveFileField object used in the method.
# def function_saveFileField( fileFieldObject):
#     logger.info("fieldFile name: "+ fileFieldObject.name)
#     fullPath=fileFieldObject.name
#     f = open(fullPath)
#     myFile =File(f)
#     partStr = fullPath.rpartition("/")
#     field=fileFieldObject.field
#     fieldFileName = partStr[2]
#     relativeFilePath = field.upload_to + fieldFileName
#     # logger.info(fieldFileName)
#     # logger.info("Before fileFieldObject.save(): Batches {batch}\n\t and samples{sample}".format(batch=str(Batch.objects.all()), sample=str(Sample.objects.all()) ))
#     fileFieldObject.save(fieldFileName,myFile)
#     # fileFieldObject=relativeFilePath
#     return relativeFilePath


@shared_task
def add(x,y):
    return x + y

@shared_task
def celery_extractDataFromCsv( csvTup):
    logger.info("getDataFromCsv reached")
    csvObj = Csv.objects.get(pk=csvTup[0])
    cName = csvObj.csvFile
    csvList = csvTup[1]
    refList = []
    batchList = []

    for row in csvList:
        thisReference = row['ReferenceFile']
        #  fileObj = open(thisReference, "r")
        # fileDict = {thisReference: fileObj}
        
    #If we already have a file with that name, we do not save.
        if not Reference.objects.filter(referenceFile=thisReference).exists():
            ref = Reference(referenceFile=thisReference)
            ref.save()
            logger.info("reference:" + str(ref.referenceFile))
            newReferenceFileName = saveFileField(ref.referenceFile)
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
    # self.doneExtracting.set()

