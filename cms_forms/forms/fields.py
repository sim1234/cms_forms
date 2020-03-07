import logging

from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import FormField


class BaseFormFieldForm(forms.ModelForm):
    class Meta:
        model = FormField
        fields = ("name", )

    field_type = None
    field_parameters = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_field_kwargs()

    def load_field_kwargs(self):
        kwargs = self.instance.kwargs
        for param in self.field_parameters:
            field = self.fields[param]
            field.initial = kwargs.get(param, field.initial)

    def get_field_kwargs(self):
        return {param: self.cleaned_data[param] for param in self.field_parameters}

    def update_instance(self):
        self.instance.kwargs = self.get_field_kwargs()
        self.instance.field_type = self.field_type

    def clean(self):
        super().clean()
        try:
            self.update_instance()
            self.instance.build_field()
        except Exception as e:
            logging.exception("Form field creation failed")
            raise forms.ValidationError(_("Form field creation failed: %(error)s"), params={"error": e})


class FormFieldForm(BaseFormFieldForm):
    field_type = "FormField"
    field_parameters = BaseFormFieldForm.field_parameters + ["required", "label", "help_text", "show_hidden_initial", "localize", "disabled", "label_suffix"]

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


class CharFieldForm(FormFieldForm):
    field_type = "CharField"
    field_parameters = FormFieldForm.field_parameters + ["max_length", "min_length", "strip", "empty_value"]

    max_length = forms.IntegerField(required=False, min_value=0)
    min_length = forms.IntegerField(required=False, min_value=0)
    strip = forms.BooleanField(required=False, initial=True)
    empty_value = forms.CharField(required=False, empty_value="")


class IntegerFieldForm(FormFieldForm):
    field_type = "IntegerField"
    field_parameters = FormFieldForm.field_parameters + ["max_value", "min_value"]

    max_value = forms.IntegerField(required=False)
    min_value = forms.IntegerField(required=False)


class FloatFieldForm(IntegerFieldForm):
    field_type = "FloatField"

    max_value = forms.FloatField(required=False)
    min_value = forms.FloatField(required=False)


class DecimalFieldForm(IntegerFieldForm):
    field_type = "DecimalField"
    field_parameters = IntegerFieldForm.field_parameters + ["max_digits", "decimal_places"]

    max_value = forms.DecimalField(required=False)
    min_value = forms.DecimalField(required=False)
    max_digits = forms.IntegerField(required=False)
    decimal_places = forms.IntegerField(required=False)


class BaseTemporalFieldForm(FormFieldForm):
    field_type = "BaseTemporalField"

    input_formats = None  # TODO


class DateFieldForm(BaseTemporalFieldForm):
    field_type = "DateField"


class TimeFieldForm(BaseTemporalFieldForm):
    field_type = "TimeField"


class DateTimeFieldForm(BaseTemporalFieldForm):
    field_type = "DateTimeField"


class DurationFieldForm(FormFieldForm):
    field_type = "DurationField"


class RegexFieldForm(CharFieldForm):
    field_type = "RegexField"
    field_parameters = CharFieldForm.field_parameters + ["regex"]

    strip = forms.BooleanField(required=False, initial=False)
    regex = forms.CharField()


class EmailFieldForm(CharFieldForm):
    field_type = "EmailField"
    field_parameters = [p for p in CharFieldForm.field_parameters if p != "strip"]

    strip = None


class FileFieldForm(FormFieldForm):
    field_type = "FileField"
    field_parameters = FormFieldForm.field_parameters + ["max_length", "allow_empty_file"]

    max_length = forms.IntegerField(required=False, min_value=0)
    allow_empty_file = forms.BooleanField(required=False, initial=False)


class ImageFieldForm(FileFieldForm):
    field_type = "ImageField"


class URLFieldForm(CharFieldForm):
    field_type = "URLField"
    field_parameters = [p for p in CharFieldForm.field_parameters if p != "strip"]

    strip = None


class BooleanFieldForm(FormFieldForm):
    field_type = "BooleanField"


class NullBooleanFieldForm(BooleanFieldForm):
    field_type = "NullBooleanField"


class ChoiceFieldForm(FormFieldForm):
    field_type = "ChoiceField"

    # choices  # TODO


class TypedChoiceFieldForm(ChoiceFieldForm):
    field_type = "TypedChoiceField"
    # TODO


class MultipleChoiceFieldForm(ChoiceFieldForm):
    field_type = "MultipleChoiceField"
    # TODO


class TypedMultipleChoiceFieldForm(ChoiceFieldForm):
    field_type = "TypedMultipleChoiceField"
    # TODO


class ComboFieldForm(FormFieldForm):
    field_type = "ComboField"
    # TODO?


class MultiValueFieldForm(FormFieldForm):
    field_type = "MultiValueField"
    # TODO?


class FilePathFieldForm(ChoiceFieldForm):
    field_type = "FilePathField"
    field_parameters = ChoiceFieldForm.field_parameters + ["path", "match", "recursive", "allow_files", "allow_folders"]

    path = forms.CharField()
    match = forms.CharField(required=False, empty_value=None)
    recursive = forms.BooleanField(required=False, initial=False)
    allow_files = forms.BooleanField(required=False, initial=True)
    allow_folders = forms.BooleanField(required=False, initial=False)


class SplitDateTimeFieldForm(MultiValueFieldForm):
    field_type = "SplitDateTimeField"

    # TODO
    input_date_formats = None
    input_time_formats = None


class GenericIPAddressFieldForm(CharFieldForm):
    field_type = "GenericIPAddressField"
    field_parameters = CharFieldForm.field_parameters + ["protocol", "unpack_ipv4"]

    protocol = forms.ChoiceField(choices=(("ipv4", "IPv4"), ("ipv6", "IPv6"), ("both", _("Both"))), initial="both")
    unpack_ipv4 = forms.BooleanField(required=False, initial=False)


class SlugFieldForm(CharFieldForm):
    field_type = "SlugField"
    field_parameters = CharFieldForm.field_parameters + ["allow_unicode"]

    allow_unicode = forms.BooleanField(required=False, initial=False)


class UUIDFieldForm(CharFieldForm):
    field_type = "UUIDField"


