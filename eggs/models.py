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


#This is for each sample
class Sample(models.Model):
    #This refers to the reference file associated with each genetic sample
    reference = models.ForeignKey(Reference, on_delete=models.DO_NOTHING)
    #This is a char field because there is no reason why the submission name needs to be super long.
    #   The first argument to CharField is intended as a human readable name.
    batch = models.CharField( max_length=100)
    sampleFile = models.FileField(upload_to="sample") 
    def __str__(self):
        return self.sampleFile.name
     #This is so VSC doesn't complain. 
    objects = models.Manager()
    
    



