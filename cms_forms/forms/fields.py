import logging

from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import FormField
from ..importer import TypeReference


class BaseFieldForm(forms.ModelForm):
    class Meta:
        model = FormField
        fields = ("name",)

    field_type = None
    field_parameters = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_field_kwargs()

    def load_field_kwargs(self):
        kwargs = self.instance.field_parameters
        for param in self.field_parameters:
            field = self.fields[param]
            field.initial = kwargs.get(param, field.initial)

    def get_field_kwargs(self):
        return {param: self.cleaned_data[param] for param in self.field_parameters}

    def update_instance(self):
        self.instance.field_parameters = self.get_field_kwargs()
        self.instance.field_type = self.field_type

    def clean(self):
        super().clean()
        try:
            self.update_instance()
            self.instance.build_field()
        except Exception as e:
            logging.exception("Form field creation failed")
            raise forms.ValidationError(_("Form field creation failed: %(error)s"), params={"error": e})


class FieldForm(BaseFieldForm):
    field_type = TypeReference("django.forms.fields.Field")
    field_parameters = BaseFieldForm.field_parameters + [
        "required",
        "label",
        "help_text",
        "show_hidden_initial",
        "localize",
        "disabled",
        "label_suffix",
    ]

    required = forms.BooleanField(required=False, initial=True)
    widget = None  # TODO
    label = forms.CharField(required=False, empty_value=None)
    initial = None  # TODO
    help_text = forms.CharField(required=False, empty_value=None)
    error_messages = None  # TODO?
    show_hidden_initial = forms.BooleanField(required=False, initial=False)
    validators = ()  # TODO
    localize = forms.BooleanField(required=False, initial=False)
    disabled = forms.BooleanField(required=False, initial=False)
    label_suffix = forms.CharField(required=False, empty_value=None)


class CharFieldForm(FieldForm):
    field_type = TypeReference("django.forms.fields.CharField")
    field_parameters = FieldForm.field_parameters + ["max_length", "min_length", "strip", "empty_value"]

    max_length = forms.IntegerField(required=False, min_value=0)
    min_length = forms.IntegerField(required=False, min_value=0)
    strip = forms.BooleanField(required=False, initial=True)
    empty_value = forms.CharField(required=False, empty_value="")


class IntegerFieldForm(FieldForm):
    field_type = TypeReference("django.forms.fields.IntegerField")
    field_parameters = FieldForm.field_parameters + ["max_value", "min_value"]

    max_value = forms.IntegerField(required=False)
    min_value = forms.IntegerField(required=False)


class FloatFieldForm(IntegerFieldForm):
    field_type = TypeReference("django.forms.fields.FloatField")

    max_value = forms.FloatField(required=False)
    min_value = forms.FloatField(required=False)


class DecimalFieldForm(IntegerFieldForm):
    field_type = TypeReference("django.forms.fields.DecimalField")
    field_parameters = IntegerFieldForm.field_parameters + ["max_digits", "decimal_places"]

    max_value = forms.DecimalField(required=False)
    min_value = forms.DecimalField(required=False)
    max_digits = forms.IntegerField(required=False)
    decimal_places = forms.IntegerField(required=False)


class BaseTemporalFieldForm(FieldForm):
    field_type = TypeReference("django.forms.fields.BaseTemporalField")

    input_formats = None  # TODO


class DateFieldForm(BaseTemporalFieldForm):
    field_type = TypeReference("django.forms.fields.DateField")


class TimeFieldForm(BaseTemporalFieldForm):
    field_type = TypeReference("django.forms.fields.TimeField")


class DateTimeFieldForm(BaseTemporalFieldForm):
    field_type = TypeReference("django.forms.fields.DateTimeField")


class DurationFieldForm(FieldForm):
    field_type = TypeReference("django.forms.fields.DurationField")


class RegexFieldForm(CharFieldForm):
    field_type = TypeReference("django.forms.fields.RegexField")
    field_parameters = CharFieldForm.field_parameters + ["regex"]

    strip = forms.BooleanField(required=False, initial=False)
    regex = forms.CharField()


class EmailFieldForm(CharFieldForm):
    field_type = TypeReference("django.forms.fields.EmailField")
    field_parameters = [p for p in CharFieldForm.field_parameters if p != "strip"]

    strip = None


class FileFieldForm(FieldForm):
    field_type = TypeReference("django.forms.fields.FileField")
    field_parameters = FieldForm.field_parameters + ["max_length", "allow_empty_file"]

    max_length = forms.IntegerField(required=False, min_value=0)
    allow_empty_file = forms.BooleanField(required=False, initial=False)


class ImageFieldForm(FileFieldForm):
    field_type = TypeReference("django.forms.fields.ImageField")


class URLFieldForm(CharFieldForm):
    field_type = TypeReference("django.forms.fields.URLField")
    field_parameters = [p for p in CharFieldForm.field_parameters if p != "strip"]

    strip = None


class BooleanFieldForm(FieldForm):
    field_type = TypeReference("django.forms.fields.BooleanField")


class NullBooleanFieldForm(BooleanFieldForm):
    field_type = TypeReference("django.forms.fields.NullBooleanField")


class ChoiceFieldForm(FieldForm):
    field_type = TypeReference("django.forms.fields.ChoiceField")

    # choices  # TODO


class TypedChoiceFieldForm(ChoiceFieldForm):
    field_type = TypeReference("django.forms.fields.TypedChoiceField")
    # TODO


class MultipleChoiceFieldForm(ChoiceFieldForm):
    field_type = TypeReference("django.forms.fields.MultipleChoiceField")
    # TODO


class TypedMultipleChoiceFieldForm(ChoiceFieldForm):
    field_type = TypeReference("django.forms.fields.TypedMultipleChoiceField")
    # TODO


class ComboFieldForm(FieldForm):
    field_type = TypeReference("django.forms.fields.ComboField")
    # TODO?


class MultiValueFieldForm(FieldForm):
    field_type = TypeReference("django.forms.fields.MultiValueField")
    # TODO?


class FilePathFieldForm(ChoiceFieldForm):
    field_type = TypeReference("django.forms.fields.FilePathField")
    field_parameters = ChoiceFieldForm.field_parameters + ["path", "match", "recursive", "allow_files", "allow_folders"]

    path = forms.CharField()
    match = forms.CharField(required=False, empty_value=None)
    recursive = forms.BooleanField(required=False, initial=False)
    allow_files = forms.BooleanField(required=False, initial=True)
    allow_folders = forms.BooleanField(required=False, initial=False)


class SplitDateTimeFieldForm(MultiValueFieldForm):
    field_type = TypeReference("django.forms.fields.SplitDateTimeField")

    # TODO
    input_date_formats = None
    input_time_formats = None


class GenericIPAddressFieldForm(CharFieldForm):
    field_type = TypeReference("django.forms.fields.GenericIPAddressField")
    field_parameters = CharFieldForm.field_parameters + ["protocol", "unpack_ipv4"]

    protocol = forms.ChoiceField(choices=(("ipv4", "IPv4"), ("ipv6", "IPv6"), ("both", _("Both"))), initial="both")
    unpack_ipv4 = forms.BooleanField(required=False, initial=False)


class SlugFieldForm(CharFieldForm):
    field_type = TypeReference("django.forms.fields.SlugField")
    field_parameters = CharFieldForm.field_parameters + ["allow_unicode"]

    allow_unicode = forms.BooleanField(required=False, initial=False)


class UUIDFieldForm(CharFieldForm):
    field_type = TypeReference("django.forms.fields.UUIDField")
