# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.files import File


# Create your models here.

class Reference(models.Model):
# This is our primary key which auto-increments
    
    referenceID = models.AutoField(primary_key=True)
    referenceFile = models.FileField(upload_to="reference/")  
    def __str__(self):
        return self.referenceFile.name
    #This is so VSC doesn't complain. 
    objects = models.Manager()

# This is for each batch
class Batch(models.Model):

    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    #We want the batchName to be unique.
    batchName = models.CharField(primary_key=True, max_length=100, unique =True)
    ## This allows us to record when the time is created. Normally, we don't want the users to input this. 
    timeCreated = models.DateTimeField(auto_now_add=True)
    objects= models.Manager()
    def __str__(self):
        return self.batchName
    


#This is for each sample
class Sample(models.Model):
    #This refers to the reference file associated with each genetic sample
   # reference = models.ForeignKey(Reference, on_delete=models.DO_NOTHING)
    #This is a char field because there is no reason why the submission name needs to be super long.
    #   The first argument to CharField is intended as a human readable name.
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    sampleFile = models.FileField(upload_to="sample") 
    def __str__(self):
        return self.sampleFile.name()
     #This is so VSC doesn't complain. 
    objects = models.Manager()



# this is for the result. One-to-one relation with batch
class Result(models.Model): 
    batch = models.OneToOneField(Batch, on_delete=models.CASCADE)  
# this should be separate because the results are generated at a different time 
# as the batch; the result creation is not instantenous!
    timeCreated = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return ("resultOf_"+str(self.batch))
    #This is so VSC doesn't complain. 
    objects = models.Manager()

class VCFRow(models.Model):
    #this is just in case we want to store the contents
    # of more than one VCF file here.
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    # def __str__(self): 
    objects = models.Manager()
    
    



