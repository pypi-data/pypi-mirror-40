# Django Imports
from django.db import models
# Django COS Imports
from django_cos.widgets import ColorPickerWidget

class ColorField(models.CharField):    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorPickerWidget
        return super(ColorField, self).formfield(**kwargs)
