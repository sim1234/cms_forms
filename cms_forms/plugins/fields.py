from cms.plugin_base import CMSPluginBase
from django.utils.translation import gettext_lazy as _

from ..models import FormField
from ..forms import fields
from .. import config


def extra_fieldset(form, exclude=None, name=None):
    if exclude is None:
        exclude = fields.FieldForm.field_parameters
    _fields = [f for f in form.field_parameters if f not in exclude]
    if _fields:
        return [(name, {"fields": _fields})]
    return []


class FormFieldPlugin(CMSPluginBase):
    module = _("Form Fields")
    model = FormField
    name = _("Field")
    render_template = "cms_forms/formfieldplugin.html"
    field_template = "cms_forms/field.html"
    form = fields.FieldForm
    fieldsets = extra_fieldset(fields.FieldForm, exclude=[], name=_("Base field parameters"))
    allow_children = True
    child_classes = config.WIDGET_PLUGIN_NAMES

    def render(self, *args, **kwargs):
        context = super().render(*args, **kwargs)
        context["plugin"] = self
        return context


class CharFieldPlugin(FormFieldPlugin):
    name = _("Char field")
    form = fields.CharFieldForm
    fieldsets = extra_fieldset(fields.CharFieldForm) + FormFieldPlugin.fieldsets


class IntegerFieldPlugin(FormFieldPlugin):
    name = _("Integer field")
    form = fields.IntegerFieldForm
    fieldsets = extra_fieldset(fields.IntegerFieldForm) + FormFieldPlugin.fieldsets


class FloatFieldPlugin(IntegerFieldPlugin):
    name = _("Float field")
    form = fields.FloatFieldForm
    fieldsets = extra_fieldset(fields.FloatFieldForm) + IntegerFieldPlugin.fieldsets


class DecimalFieldPlugin(IntegerFieldPlugin):
    name = _("Decimal field")
    form = fields.DecimalFieldForm
    fieldsets = extra_fieldset(fields.DecimalFieldForm) + IntegerFieldPlugin.fieldsets


class BaseTemporalFieldPlugin(FormFieldPlugin):
    pass


class DateFieldPlugin(BaseTemporalFieldPlugin):
    name = _("Date field")
    form = fields.DateFieldForm
    fieldsets = extra_fieldset(fields.DateFieldForm) + BaseTemporalFieldPlugin.fieldsets


class TimeFieldPlugin(BaseTemporalFieldPlugin):
    name = _("Time field")
    form = fields.TimeFieldForm
    fieldsets = extra_fieldset(fields.TimeFieldForm) + BaseTemporalFieldPlugin.fieldsets


class DateTimeFieldPlugin(BaseTemporalFieldPlugin):
    name = _("DateTime field")
    form = fields.DateTimeFieldForm
    fieldsets = extra_fieldset(fields.DateTimeFieldForm) + BaseTemporalFieldPlugin.fieldsets


class DurationFieldPlugin(FormFieldPlugin):
    name = _("Duration field")
    form = fields.DurationFieldForm
    fieldsets = extra_fieldset(fields.DurationFieldForm) + FormFieldPlugin.fieldsets


class RegexFieldPlugin(CharFieldPlugin):
    name = _("Regex field")
    form = fields.RegexFieldForm
    fieldsets = extra_fieldset(fields.RegexFieldForm) + CharFieldPlugin.fieldsets


class EmailFieldPlugin(CharFieldPlugin):
    name = _("Email field")
    form = fields.EmailFieldForm
    fieldsets = extra_fieldset(fields.EmailFieldForm) + extra_fieldset(
        fields.CharFieldForm, exclude=["strip"], name=_("Base field parameters")
    )


class FileFieldPlugin(FormFieldPlugin):
    name = _("File field")
    form = fields.FileFieldForm
    fieldsets = extra_fieldset(fields.FileFieldForm) + FormFieldPlugin.fieldsets


class ImageFieldPlugin(FileFieldPlugin):
    name = _("Image field")
    form = fields.ImageFieldForm
    fieldsets = extra_fieldset(fields.ImageFieldForm) + FileFieldPlugin.fieldsets


class URLFieldPlugin(CharFieldPlugin):
    name = _("URL field")
    form = fields.URLFieldForm
    fieldsets = extra_fieldset(fields.URLFieldForm) + extra_fieldset(
        fields.CharFieldForm, exclude=["strip"], name=_("Base field parameters")
    )


class BooleanFieldPlugin(FormFieldPlugin):
    name = _("Boolean field")
    form = fields.BooleanFieldForm
    fieldsets = extra_fieldset(fields.BooleanFieldForm) + FormFieldPlugin.fieldsets


class NullBooleanFieldPlugin(BooleanFieldPlugin):
    name = _("NullBoolean field")
    form = fields.NullBooleanFieldForm
    fieldsets = extra_fieldset(fields.NullBooleanFieldForm) + BooleanFieldPlugin.fieldsets


class ChoiceFieldPlugin(FormFieldPlugin):
    name = _("Choice field")
    form = fields.ChoiceFieldForm
    fieldsets = extra_fieldset(fields.ChoiceFieldForm) + FormFieldPlugin.fieldsets
    child_classes = FormFieldPlugin.child_classes + config.CHOICE_OPTION_PLUGIN_NAMES


class TypedChoiceFieldPlugin(ChoiceFieldPlugin):
    name = _("TypedChoice field")
    form = fields.TypedChoiceFieldForm
    fieldsets = extra_fieldset(fields.TypedChoiceFieldForm) + ChoiceFieldPlugin.fieldsets


class MultipleChoiceFieldPlugin(ChoiceFieldPlugin):
    name = _("MultipleChoice field")
    form = fields.MultipleChoiceFieldForm
    fieldsets = extra_fieldset(fields.MultipleChoiceFieldForm) + ChoiceFieldPlugin.fieldsets


class TypedMultipleChoiceFieldPlugin(ChoiceFieldPlugin):
    name = _("TypedMultipleChoice field")
    form = fields.TypedMultipleChoiceFieldForm
    fieldsets = extra_fieldset(fields.TypedMultipleChoiceFieldForm) + ChoiceFieldPlugin.fieldsets


class ComboFieldPlugin(FormFieldPlugin):
    name = _("Combo field")
    form = fields.ComboFieldForm
    fieldsets = extra_fieldset(fields.ComboFieldForm) + FormFieldPlugin.fieldsets


class MultiValueFieldPlugin(FormFieldPlugin):
    name = _("MultiValue field")
    form = fields.MultiValueFieldForm
    fieldsets = extra_fieldset(fields.MultiValueFieldForm) + FormFieldPlugin.fieldsets


class FilePathFieldPlugin(ChoiceFieldPlugin):
    name = _("FilePath field")
    form = fields.FilePathFieldForm
    fieldsets = extra_fieldset(fields.FilePathFieldForm) + ChoiceFieldPlugin.fieldsets


class SplitDateTimeFieldPlugin(MultiValueFieldPlugin):
    name = _("SplitDateTime field")
    form = fields.SplitDateTimeFieldForm
    fieldsets = extra_fieldset(fields.SplitDateTimeFieldForm) + MultiValueFieldPlugin.fieldsets


class GenericIPAddressFieldPlugin(CharFieldPlugin):
    name = _("GenericIPAddress field")
    form = fields.GenericIPAddressFieldForm
    fieldsets = extra_fieldset(fields.GenericIPAddressFieldForm) + CharFieldPlugin.fieldsets


class SlugFieldPlugin(CharFieldPlugin):
    name = _("Slug field")
    form = fields.SlugFieldForm
    fieldsets = extra_fieldset(fields.SlugFieldForm) + CharFieldPlugin.fieldsets


class UUIDFieldPlugin(CharFieldPlugin):
    name = _("UUID field")
    form = fields.UUIDFieldForm
    fieldsets = extra_fieldset(fields.UUIDFieldForm) + CharFieldPlugin.fieldsets
