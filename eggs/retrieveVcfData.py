import psycopg2 
from subprocess import call
from eggs.models import VCFRow
from django.db.models import F
import os


def storeVcf(vcfFileName):
    conn = psycopg2.connect("""dbname=cardinal 
    user=gamel port=5433""")
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
def extractFromFormat():
    # conn = psycopg2.connect("""dbname=cardinal 
    # user=gamel port=5433""")
    # cur = conn.cursor()
    # listOfRows = []
    # this makes all the format fields available as a dictionary
    for row in VCFRow.objects.iterator():
        
        # nameList = row.formatNameColInFile.split(':')
        # valueList = row.formatValueColInFile.split(':')
        # formatDict = dict(zip(nameList, valueList))
        # this gets the FORNMAT (filtered) read depth
        # totalDepth = formatDict['DP']
        # row.formatDP = int(totalDepth)
        # we need to separate the AD string into the re
        # relevant parts
        # adString = formatDict['AD']
        # adList = adString.split(',')
     
        # row.formatRefAlleleReads = int(adList[0])
        # row.formatAltAlleleReads = int(adList[1])
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
	        # infoKey.append(infoElement[0])
            # if (length == 1):
            #     infoValue.append(None)
            # else: 
	        #     infoValue.append(infoElement[1])
        infoDict = dict(zip(infoKey,infoValue))
        row.infoDP = infoDict['DP']
        infoADString = infoDict['AD']
        infoAD = infoADString.split(',')

        row.infoRefAlleleReads = int(infoAD[0])
        row.infoAltAlleleReads = int(infoAD[1])
        row.save()
# row.save()
        #Get columns from formatDict
        # listOfRows.append({ thisRowId: formatDict
        # })
       
    # hopefully this will do a bulk save
    # # the bulk of the function is here. 
    # cur.close()
    # conn.close()

def calculateVariants():
    
    return VCFRow.objects.filter(infoAltAlleleReads__gt=F('infoDP') * .50).count()


def exportToJson():
    significantVariantCount = calculateVariants
    totalCount = VCFRow.objects.filter.all().count()
