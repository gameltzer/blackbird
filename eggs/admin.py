# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Reference,Sample, Batch,Result,VCFRow

# Register your models here.
admin.site.register(Reference)
admin.site.register(Sample)
admin.site.register(Batch)
admin.site.register(Result)
admin.site.register(VCFRow)
