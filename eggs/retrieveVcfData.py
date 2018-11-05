import psycopg2 
from subprocess import call
from eggs.models import VCFRow, Result, CSV
from django.db.models import F
import os
from django.core import serializers
from django.conf import settings

db = settings.DATABASES["default"]


def storeVcf(vcfFileName):
    conn = psycopg2.connect("dbname="+ db['NAME'] + " "+ "user="+ db['USER'] + " "+ "password=" + " "b['PASSWORD'] + " " +
    "port="+ db['PORT'] + "host="+db["HOST"])
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
    for row in VCFWithoutResult.iterator():
      
        row.result = result
            # this gets the unfiltered DP ( we want unfiltered just like the AD)
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
        row.save()

#this calculates how many variants
def calculateVariants(thisResult):
    resultRows=VCFRow.objects.filter(result=thisResult)
    thisResult.significantVariantCount = resultRows.filter(infoAltAlleleReads__gt=F('infoDP') * .50).count()
    thisResult.totalCount = resultRows.all().count()
    thisResult.save()

# this saves all our results in a json file so that javascript can use it to make the graph
def exportToJson():
    JSONSerializer = serializers.get_serializer("json")
    json_serializer = JSONSerializer()
    with open("eggs/static/eggs/resultJson.json", "w") as out:
        json_serializer.serialize(Result.objects.all(), stream=out)

# this just empties the results and VCFRow and CSV objectstables so that we can continue developing
def refresh():
    Result.objects.all().delete()
    VCFRow.objects.all().delete()
    CSV.objects.all().delete()