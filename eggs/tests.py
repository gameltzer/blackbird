 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client

# thins in example at https://docs.djangoproject.com/en/1.11/topics/testing/tools/#django.test.LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from eggs.models import Batch, Reference, Sample
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import traceback
import sys
import logging
import os
# from selenium.webdriver.common.desired_capabilties import DesiredCapabilities
from subprocess import call
from celery.contrib.testing.worker import start_worker
# from blackbird.celery import app



logger = logging.getLogger("django.server")
# Create your tests here.

# This is to figure out what's going on with tabulate. 
class TabulateTest(TestCase):
    pathOfFilesToUpload = "/mnt/LinuxLanzaProject/csvDevTest/"
    referenceFileName = "RefSalmonellaGCF000195995.1_ASM.fna"
    sample1FileName = "Salmonella_enterica_SRR8110782_1.fastq"

    sample2FileName = "Salmonella_enterica_SRR8110782_2.fastq"
    client=Client()
    

    def initialize(self): 
        session = self.client.session
        r = Reference(referenceFile=self.pathOfFilesToUpload + self.referenceFileName)
        r.save()
        b = Batch(batchName="tabulateThis", reference = r)
        b.save()
        s1 = Sample(sampleFile=self.sample1FileName, batch=b)
        s1.save()
        s2 = Sample(sampleFile=self.sample2FileName, batch=b)
        s2.save()
        session["batchName"]=b.batchName
        session.save()

  
#The not was added so it isn't treated as a test.
    def not_test_Submit(self):
        self.initialize()
        response = self.client.get('/submit')
        print(response)
        self.assertEqual(response.status_code, 200)
#The not was added so it isn't treated as a test. 
    def not_test_Tabulate(self):
        self.initialize()
        response = self.client.get('/tabulate')
        print(response)
        self.assertEqual(response.status_code, 200)

class notOnSubmit(object):
    def __call__(self, driver):
        page_source = driver.page_source
        if "Select set of files for processing" in page_source:
            return False
        else:
            print("notOnSubmit returned True")
            return True
# class NotOnSamePage(object):
#     # # This allows us to speciy the text on the page when we make a new object. 
#     def __init__(self, pageText):
#         self.pageText= pageText

#     def __call__(self, driver):
#         page_source = driver.page_source
#         #CSV is all upercase here because this is what the user is seeing.
#         if self.pageText in page_source:
#             return False
#         else:
#             print("NotOnSamePage returned True")
#             return True


class EggsTests(StaticLiveServerTestCase):
    #location of folder files will be uploaded from on linux virtual machine.
    pathOfFilesToUpload = "/mnt/LinuxLanzaProject/csvDevTest/"
    referenceFileName = "RefSalmonellaGCF000195995.1_ASM.fna"
    sample1FileName = "Salmonella_enterica_SRR8110782_1.fastq"

    sample2FileName = "Salmonella_enterica_SRR8110782_2.fastq"

    csvFilename = "sample.csv"
    #CHROME#
    @classmethod
    def setUpClass(cls):
        super(EggsTests, cls).setUpClass()
        # This allows console logging to be redirect to the django log
        # d = webdriver.DesiredCapabilities.CHROME
        # d['loggingPrefs'] = {'browser': 'ALL'}
        # cls.selenium = webdriver.chrome.webdriver.WebDriver(desired_capabilities=d)
        # cls.selenium = webdriver.chrome.webdriver.WebDriver(service_args=["--verbose","--log-path=/mnt/LinuxLanzaProject/chromium.log"])
        cls.selenium = webdriver.chrome.webdriver.WebDriver()
        # cls.selenium = webdriver.firefox.webdriver.WebDriver()
        cls.selenium.implicitly_wait(30)
        cls.selenium.set_page_load_timeout(216000)
        cls.selenium.get(cls.live_server_url)
        # cls.celery_worker = start_worker(app)
        # cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        # cls.celery_worker.__exit__()
        super(EggsTests, cls).tearDownClass()

    
    # this clicks on the button that will send us to the next page. 
    def selectUploadOption(self):
        uploadInputOptions = self.selenium.find_elements_by_class_name("uploadInputOption")
        optionElement = None  
        for option in uploadInputOptions:
            if option.is_displayed():
                optionElement = option
                break
        if optionElement == None:
            raise Exception
        optionElement.click()
    
class SingleSampleTest(EggsTests):

        # this clicks on the button which activates the javascript
    def pickSingleSampleSet(self):
        
        self.selenium.find_element_by_id('fastButton').click()
        assert "Choose how to upload files." in self.selenium.page_source

    # Picks the reference file
    def pickReference(self):
        fileUpload= self.selenium.find_element_by_name("referenceFile")

        fileUpload.clear()
        fileUpload.send_keys(self.pathOfFilesToUpload + self.referenceFileName)
    # this automates the upload reference file page
    def uploadReference(self):
        assert "Upload Reference File" in self.selenium.page_source
        self.pickReference()
        submitReference = self.selenium.find_element_by_name("submitReference")
        submitReference.click()
    
    # This selects files from drop down menus
    def selectFileFromDropDown(self,selectorElementName, desiredValue):
        select = Select(self.selenium.find_element_by_name(selectorElementName))
        select.select_by_visible_text(desiredValue)

    #this enters our test Batch
    def enterBatch(self):
        batchName = self.selenium.find_element_by_name("batchName")
        batchName.clear()
        batchName.send_keys("example")
    # This performs the acction of labeling the batch. It also selects the reference file from the menu
    # and submits.
    def labelBatch(self):
        assert "BatchName" in self.selenium.page_source
        self.enterBatch()
        self.selectFileFromDropDown("reference",str("reference/"+self.referenceFileName))
        self.selenium.find_element_by_id("submit").click()

    def pickSamples(self):
        sample1 = self.selenium.find_element_by_name("form-0-sampleFile")
        sample2 = self.selenium.find_element_by_name("form-1-sampleFile")
        sample1.clear()
        sample1.send_keys(self.pathOfFilesToUpload + self.sample1FileName)
        sample2.clear()
        sample2.send_keys(self.pathOfFilesToUpload + self.sample2FileName)


    # this uploads the sample files
    def uploadSampleFiles(self):
        assert "The batch is" in self.selenium.page_source
        self.pickSamples()
        self.selenium.find_element_by_id("submit").click()

    # this submits the references and the samples
    def submitBatch(self):
        
        assert "Select set of files for processing" in self.selenium.page_source
        self.selenium.find_element_by_id("submitBatch").click()
    
    # this tabulates the test results.
    def tabulateBatch(self):
        assert "Tabulate data from the vcf" in self.selenium.page_source
        self.selenium.find_element_by_id("submitTabulate").click()
    
    #This handles the graphing and is the end of the workflow.
    def graphBatch(self):
        assert "Number of mutations." in self.selenium.page_source

   
    def uploadSingleBatch(self, submit=True):
        assert "Upload Batch Files" in self.selenium.page_source
        self.pickReference()
        self.enterBatch()
        self.pickSamples()
        if (submit==True):
            self.selenium.find_element_by_name("uploadEntireBatch").click()

    def test_Tester(self):
        self.pickSingleSampleSet()
     
    # def test_Workflow(self):
    #     self.pickSingleSampleSet()
    #     self.selectUploadOption()
    #     self.uploadReference()
    #     self.labelBatch()
    #     self.uploadSampleFiles()
    #     self.submitBatch()
    #     wait = WebDriverWait(self.selenium, 24*7200)
    #     wait.until(notOnSubmit())
    #     # self.tabulateBatch()
    #     self.graphBatch()

    def test_ImproveEfficency(self):
        self.pickSingleSampleSet()
        self.selectUploadOption()
        self.uploadSingleBatch()
        wait = WebDriverWait(self.selenium, 24*7200)
        wait.until(EC.presence_of_element_located((By.ID, "Files for processing")))
                # wait.until(NotOnSamePage("Upload Batch Files"))

        self.submitBatch()
        # wait = WebDriverWait(self.selenium, 24*7200)
        # wait.until(NotOnSamePage("Select set of files for processing"))
        wait.until(EC.presence_of_element_located((By.ID, "graphSingle")))
        # self.tabulateBatch()
        self.graphBatch()

    @classmethod
    def tearDownClass(cls):
        pass
    
class CsvSamplesTest(EggsTests):
    def pickCsv(self):
        assert "Choose how to upload files." in self.selenium.page_source
        self.selenium.find_element_by_id("csvButton").click()
    
    def uploadCsvFiles(self):
        assert "Upload CSV File" in self.selenium.page_source
        csvFile = self.selenium.find_element_by_name("csvFile")
        csvFile.clear()
        csvFile.send_keys(self.pathOfFilesToUpload + self.csvFilename)
        self.selenium.find_element_by_id("uploadCSV").click()
        logger.info("according to the test the filename is {0}.".format(self.csvFilename))
#This is the part of the test that handles the page for sending data to the pipeline. 
    def sendBulkDataToPipeline(self):
        assert "Send data to pipeline." in self.selenium.page_source
        self.selenium.find_element_by_id("processFiles").click()

    def graphCsv(self):
        assert "Number of mutations." in self.selenium.page_source
        
    def outputLog(self):
        for entry in self.selenium.get_log('browser'):
            logger.info(entry)


    def test_Csv(self):
        # self.celery_worker()
    
        self.pickCsv()
        self.selectUploadOption()
        self.uploadCsvFiles()
        wait = WebDriverWait(self.selenium, 24*7200)
        wait.until(EC.presence_of_element_located((By.ID, "sendDataToPipeline_id" )))
        self.sendBulkDataToPipeline()
        wait = WebDriverWait(self.selenium, 24*7200)
        wait.until(EC.presence_of_element_located((By.ID, "csvGraph_id")))
        self.graphCsv()

        # except TimeoutException as ex:
        #     logger.info("\t Timeout Exception {} \n".format(str(ex)))
        #     logger.info(ex.stacktrace)
       
        # self.graphCsv()
        # self.outputLog()
   
   

    @classmethod
    def tearDownClass(cls):
        pass



    
 
