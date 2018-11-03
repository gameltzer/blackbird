from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings 

class Command(BaseCommand):
    def handle(self, *args, **options):
        myDatabase = settings.DATABASES['default']
        if not User.objects.filter(username=myDatabase['USER']).exists():
            User.objects.create_superuser(myDatabase['USER'], "gameltzer@gmail.com",myDatabase['PASSWORD'])