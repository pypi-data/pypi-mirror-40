"""
Enhancements to wagtail.contrib.forms.
"""
# Standard Library Imports
import os
import re
import csv
# Django Imports
from django import forms
from django.db import models
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# Wagtail Imports
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.contrib.forms.views import SubmissionsListView as WagtailSubmissionsListView
# Django COS Imports
from django_cos.settings import cr_settings
from django_cos.utils import attempt_protected_media_value_conversion

FORM_FIELD_CHOICES = (
    (_('Text'), (
        ('singleline', _('Single line text')),
        ('multiline', _('Multi-line text')),
        ('email', _('Email')),
        ('number', _('Number - only allows integers')),
        ('url', _('URL')),
    ),),
    (_('Choice'), (
        ('checkboxes', _('Checkboxes')),
        ('dropdown', _('Drop down')),
        ('radio', _('Radio buttons')),
        ('multiselect', _('Multiple select')),
        ('checkbox', _('Single checkbox')),
    ),),
    (_('Date & Time'), (
        ('date', _('Date')),
        ('time', _('Time')),
        ('datetime', _('Date and time')),
    ),),
    (_('File Upload'), (
        ('file', _('Secure File - login required to access uploaded files')),
        ('files', _('Secure Files - login required to access uploaded files')),
    ),),
    (_('Other'), (
        ('hidden', _('Hidden field')),
    ),),
)


# Files

class SecureFileField(forms.FileField):
    custom_error_messages = {
        'blacklist_file': _('Submitted file is not allowed.'),
        'whitelist_file': _('Submitted file is not allowed.')
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.error_messages.update(self.custom_error_messages)

    def validate(self, value):
        super(SecureFileField, self).validate(value)
        if value:
            self._check_whitelist(value)
            self._check_blacklist(value)

    def _check_whitelist(self, value):
        if cr_settings['PROTECTED_MEDIA_UPLOAD_WHITELIST']:
            if os.path.splitext(value.name)[1].lower() not in cr_settings['PROTECTED_MEDIA_UPLOAD_WHITELIST']:
                raise ValidationError(self.error_messages['whitelist_file'])

    def _check_blacklist(self, value):
        if cr_settings['PROTECTED_MEDIA_UPLOAD_BLACKLIST']:
            if os.path.splitext(value.name)[1].lower() in cr_settings['PROTECTED_MEDIA_UPLOAD_BLACKLIST']:
                raise ValidationError(self.error_messages['blacklist_file'])

class SecureFilesField(SecureFileField):
    widget = forms.widgets.FileInput(attrs={'multiple': True})


# Date

class DjangoCOSDateInput(forms.DateInput):
    template_name = 'django_cos/formfields/date.html'

class DjangoCOSDateField(forms.DateField):
    widget = DjangoCOSDateInput()


# Datetime

class DjangoCOSDateTimeInput(forms.DateTimeInput):
    template_name = 'django_cos/formfields/datetime.html'

class DjangoCOSDateTimeField(forms.DateTimeField):
    widget = DjangoCOSDateTimeInput()
    input_formats = ['%Y-%m-%dT%H:%M', '%m/%d/%Y %I:%M %p', '%m/%d/%Y %I:%M%p', '%m/%d/%Y %H:%M']


# Time

class DjangoCOSTimeInput(forms.TimeInput):
    template_name = 'django_cos/formfields/time.html'

class DjangoCOSTimeField(forms.TimeField):
    widget = DjangoCOSTimeInput()
    input_formats = ['%H:%M', '%I:%M %p', '%I:%M%p']


class DjangoCOSFormBuilder(FormBuilder):
    """
    Enhance wagtail FormBuilder with additional custom fields.
    """

    def create_file_field(self, field, options):
        return SecureFileField(**options)

    def create_date_field(self, field, options):
        return DjangoCOSDateField(**options)

    def create_datetime_field(self, field, options):
        return DjangoCOSDateTimeField(**options)

    def create_time_field(self, field, options):
        return DjangoCOSTimeField(**options)


class DjangoCOSSubmissionsListView(WagtailSubmissionsListView):
    def get_csv_response(self, context):
        filename = self.get_csv_filename()
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment;filename={}'.format(filename)

        writer = csv.writer(response)
        writer.writerow(context['data_headings'])
        for data_row in context['data_rows']:
            modified_data_row = []
            for cell in data_row:
                modified_cell = attempt_protected_media_value_conversion(self.request, cell)
                modified_data_row.append(modified_cell)

            writer.writerow(modified_data_row)
        return response


class DjangoCOSFormField(AbstractFormField):
    class Meta:
        abstract = True

    field_type = models.CharField(verbose_name=_('field type'), max_length=16, choices=FORM_FIELD_CHOICES, blank=True)


class SearchForm(forms.Form):
    s = forms.CharField(
        max_length=255,
        required=False,
        label=_('Search'),
    )
    t = forms.CharField(
        widget=forms.HiddenInput,
        max_length=255,
        required=False,
        label=_('Page type'),
    )

def get_page_model_choices():
    """
    Returns a list of tuples of all creatable DjangoCOS pages
    in the format of ("Custom DjangoCOS Page", "CustomDjangoCOSPage")
    """
    from django_cos.models import get_page_models
    print((
        (page.__name__, re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', page.__name__)) for page in get_page_models() if page.is_creatable
    ))
    return (
        (page.__name__, re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', page.__name__)) for page in get_page_models() if page.is_creatable
    )
