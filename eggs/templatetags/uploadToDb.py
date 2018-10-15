from django import template
from django.template.defaultfilters import stringfilter
# we want all the model objects avaiable
from eggs.models import Reference
register = template.Library()
# you must define an upload function on each model class you want to use.
# The object and the upload name are the input, and then the object
# calls its upload method. 

def uploadFile(value, arg):
    value.upload(arg)

@register.assignment_tag
def extractFileName(fileName):
    return str(fileName)

## registering filter
register.filter('uploadFile', uploadFile)
