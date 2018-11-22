from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

#This prevents overwriting. With help from https://stackoverflow.com/questions/9522759/imagefield-overwrite-image-file-with-same-name

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length):
        if self.exists(name):
            # removes the existing file
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name