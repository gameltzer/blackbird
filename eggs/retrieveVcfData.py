import psycopg2 
from subprocess import call
from eggs.models import VCFRow, Result, Csv
from django.db.models import F
import os
from django.core import serializers
from django.conf import settings
import logging
from django.core.files import File

db = settings.DATABASES["default"]

logger = logging.getLogger("django.server")

def storeVcf(vcfFileName):
    conn = psycopg2.connect("dbname="+ db['NAME'] + " "+ "user="+ db['USER'] + " "+ "password=" + db['PASSWORD'] + " " +
    "port="+ str(db['PORT']) +" "+
     "host="+db["HOST"])
    cur = conn.cursor()
    cleanVcfFileName = "clean"+ vcfFileName
    cleanVcfFile = open(cleanVcfFileName, "w+")
    #commandText= "grep -v '^#' "+ vcfFileName + " > " + cleanVcfFileName
    call(["grep", "-v", "^#", vcfFileName], 
        stdout =cleanVcfFile
    )
    cleanVcfFile.flush()
    cleanVcfFile.seek(0)
    cur.copy_from(cleanVcfFile, 'eggs_vcfrow',sep="\t",
    columns=('"chrom"','"pos"','"idColInFile"','"ref"',
    '"alt"','"qual"','"filterColInFile"','"info"',
    '"formatNameColInFile"','"formatValueColInFile"'))
  #  except StandardEror(err):
   #     print("Error:"+ err)
     # returns to previous directory
    cleanVcfFile.close()
    conn.commit()
    cur.close()
  

    conn.close()

#this if for only one vcfFile stored in vcfRow  
# It puts the ad and DP information into separate columns  
def extractFromFormat(result):
    VCFWithoutResult = VCFRow.objects.filter(result__isnull=True)
    logger.info(VCFWithoutResult)
    for row in VCFWithoutResult.iterator():
        # logger.info("row result: "+ str(row.result) + " ; input result: " + str(result))
        row.result = result
            # this gets the unfiltered DP ( we want unfiltered just like the AD)
        logger.info("row result: "+ str(row.result.id) + " ; input result: " + str(result.id))
        info = row.info.split(";")
        for i in range(len( info)):
            infoList = info[i].split("=")
            info[i] = infoList
        infoKey = []
        infoValue = []
        infoDict = {}
        for infoElement in info:
            infoKey.append(infoElement[0])
            length = len(infoElement)
            if (length == 1):
                infoValue.append(".")
            else:
                infoValue.append(infoElement[1])
        
        infoDict = dict(zip(infoKey,infoValue))
        row.infoDP = infoDict['DP']
        infoADString = infoDict['AD']
        infoAD = infoADString.split(',')

        row.infoRefAlleleReads = int(infoAD[0])
        row.infoAltAlleleReads = int(infoAD[1])
        logger.info("row:" + str(row.infoRefAlleleReads))
        row.save()

#this calculates how many variants
def calculateVariants(thisResult):
    logger.info("Calculate Variants Step Reached")
    resultRows=VCFRow.objects.filter(result=thisResult)
    thisResult.significantVariantCount = resultRows.filter(infoAltAlleleReads__gt=F('infoDP') * .50).count()
    thisResult.totalCount = resultRows.all().count()
    thisResult.save()

# this saves all our results in a json file so that javascript can use it to make the graph
def exportToJson(results):
    logger.info("exportToJson step reached")
    JSONSerializer = serializers.get_serializer("json")
    json_serializer = JSONSerializer()
    with open("eggs/static/eggs/resultJson.json", "w") as out:
        json_serializer.serialize(results, stream=out)

def exportToJsonCsv(resultList):
#     pass
    JSONSerializer = serializers.get_serializer("json")
    json_serializer = JSONSerializer()
    with open("eggs/static/eggs/resultJson.json", "w") as out:
        json_serializer.serialize(resultList, stream=out)
    

# # # this just empties the results and VCFRow and CSV objectstables so that we can continue developing
# def refresh():
#     Result.objects.all().delete()
#     VCFRow.objects.all().delete()
#     Csv.objects.all().delete()

# this takes the fileFieldObject and saves it the media directory. This must be done since we are working directly with the model
# rather than a form or modelform. The object returns is the new name of the fieldFile.... the model object must be updated to reflect.
# Tnis is a function because we might want to use itin different classes and views.
def saveFileField(fileFieldObject):
    logger.info("fieldFile name: "+ fileFieldObject.name)
    fullPath=fileFieldObject.name
    f = open(fullPath)
    myFile =File(f)
    partStr = fullPath.rpartition("/")
    field=fileFieldObject.field
    fieldFileName = partStr[2]
    relativeFilePath = field.upload_to + fieldFileName
    # logger.info(fieldFileName)
    # logger.info("Before fileFieldObject.save(): Batches {batch}\n\t and samples{sample}".format(batch=str(Batch.objects.all()), sample=str(Sample.objects.all()) ))
    fileFieldObject.save(fieldFileName,myFile)
    # fileFieldObject=relativeFilePath
    return relativeFilePath