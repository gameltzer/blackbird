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
import traceback
import sys
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
class NotOnUploadCsv(object):
    def __call__(self, driver):
        page_source = driver.page_source
        if "Upload Csv File" in page_source:
            return False
        else:
            print("notOnSubmit returned True")
            return True


class EggsTests(StaticLiveServerTestCase):
    #location of folder files will be uploaded from on linux virtual machine.
    pathOfFilesToUpload = "/mnt/LinuxLanzaProject/csvDevTest/"
    referenceFileName = "RefSalmonellaGCF000195995.1_ASM.fna"
    sample1FileName = "Salmonella_enterica_SRR8110782_1.fastq"

    sample2FileName = "Salmonella_enterica_SRR8110782_2.fastq"
    csvFilename = "sample.csv"
    @classmethod
    def setUpClass(cls):
        super(EggsTests, cls).setUpClass()
        cls.selenium = webdriver.chrome.webdriver.WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.get(cls.live_server_url)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
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
    # this automates the upload reference file page
    def uploadReference(self):
        assert "Upload Reference File" in self.selenium.page_source
        fileUpload= self.selenium.find_element_by_name("referenceFile")
        submitReference = self.selenium.find_element_by_name("submitReference")
        fileUpload.clear()
        fileUpload.send_keys(self.pathOfFilesToUpload + self.referenceFileName)
        submitReference.click()
    
    # This selects files from drop down menus
    def selectFileFromDropDown(self,selectorElementName, desiredValue):
        select = Select(self.selenium.find_element_by_name(selectorElementName))
        select.select_by_visible_text(desiredValue)

    # This performs the acction of labeling the batch. It also selects the reference file from the menu
    # and submits.
    def labelBatch(self):
        assert "BatchName" in self.selenium.page_source
        batchName = self.selenium.find_element_by_name("batchName")
        batchName.clear()
        batchName.send_keys("example")
        self.selectFileFromDropDown("reference",str("reference/"+self.referenceFileName))
        self.selenium.find_element_by_id("submit").click()

    # this uploads the sample files
    def uploadSampleFiles(self):
        assert "The batch is" in self.selenium.page_source
        sample1 = self.selenium.find_element_by_name("form-0-sampleFile")
        sample2 = self.selenium.find_element_by_name("form-1-sampleFile")
        sample1.clear()
        sample1.send_keys(self.pathOfFilesToUpload + self.sample1FileName)
        sample2.clear()
        sample2.send_keys(self.pathOfFilesToUpload + self.sample2FileName)
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

   

        
    def test_Tester(self):
        self.pickSingleSampleSet()
     
    def test_Workflow(self):
        self.pickSingleSampleSet()
        self.selectUploadOption()
        self.uploadReference()
        self.labelBatch()
        self.uploadSampleFiles()
        self.submitBatch()
        wait = WebDriverWait(self.selenium, 24*7200)
        wait.until(notOnSubmit())
        self.tabulateBatch()
        self.graphBatch()
    
class CsvSamplesTest(EggsTests):
    def pickCsv(self):
        assert "Choose how to upload files." in self.selenium.page_source
        self.selenium.find_element_by_id("csvButton").click()
    
    def uploadCsvFiles(self):
        assert "Upload CSV File" in self.selenium.page_source
        csvFile = self.selenium.find_element_by_name("csvFile")
        csvFile.clear()
        csvFile.send_keys(self.pathOfFilesToUpload + self.csvFilename)
        self.selenium.find_element_by_id("submitCSV").click()
    def graphCsv(self):
        assert "Number of mutations." in self.selenium.page_source
        

    def test_Csv(self):
        self.pickCsv()
        self.selectUploadOption()
        self.uploadCsvFiles()
        # wait = WebDriverWait(self.selenium, 24*7200)
        # wait.until(NotOnUploadCsv())
        # self.graphCsv()
    
    @classmethod
    def tearDownClass(cls):
        pass



    
 
