from cms.plugin_base import CMSPluginBase
from django.utils.translation import gettext_lazy as _

from ..models import FormField
from ..forms import fields
from .. import config


class FormFieldPlugin(CMSPluginBase):
    module = _("Form Fields")
    model = FormField
    name = _("Field")
    render_template = "cms_forms/field.html"
    form = fields.FieldForm
    allow_children = True
    child_classes = config.WIDGET_PLUGIN_NAMES


class CharFieldPlugin(FormFieldPlugin):
    name = _("Char field")
    form = fields.CharFieldForm


class IntegerFieldPlugin(FormFieldPlugin):
    name = _("Integer field")
    form = fields.IntegerFieldForm


class FloatFieldPlugin(IntegerFieldPlugin):
    name = _("Float field")
    form = fields.FloatFieldForm


class DecimalFieldPlugin(IntegerFieldPlugin):
    name = _("Decimal field")
    form = fields.DecimalFieldForm


class BaseTemporalFieldPlugin(FormFieldPlugin):
    pass


class DateFieldPlugin(BaseTemporalFieldPlugin):
    name = _("Date field")
    form = fields.DateFieldForm


class TimeFieldPlugin(BaseTemporalFieldPlugin):
    name = _("Time field")
    form = fields.TimeFieldForm


class DateTimeFieldPlugin(BaseTemporalFieldPlugin):
    name = _("DateTime field")
    form = fields.DateTimeFieldForm


class DurationFieldPlugin(FormFieldPlugin):
    name = _("Duration field")
    form = fields.DurationFieldForm


class RegexFieldPlugin(CharFieldPlugin):
    name = _("Regex field")
    form = fields.RegexFieldForm


class EmailFieldPlugin(CharFieldPlugin):
    name = _("Email field")
    form = fields.EmailFieldForm


class FileFieldPlugin(FormFieldPlugin):
    name = _("File field")
    form = fields.FileFieldForm


class ImageFieldPlugin(FileFieldPlugin):
    name = _("Image field")
    form = fields.ImageFieldForm


class URLFieldPlugin(CharFieldPlugin):
    name = _("URL field")
    form = fields.URLFieldForm


class BooleanFieldPlugin(FormFieldPlugin):
    name = _("Boolean field")
    form = fields.BooleanFieldForm


class NullBooleanFieldPlugin(BooleanFieldPlugin):
    name = _("NullBoolean field")
    form = fields.NullBooleanFieldForm


class ChoiceFieldPlugin(FormFieldPlugin):
    name = _("Choice field")
    form = fields.ChoiceFieldForm


class TypedChoiceFieldPlugin(ChoiceFieldPlugin):
    name = _("TypedChoice field")
    form = fields.TypedChoiceFieldForm


class MultipleChoiceFieldPlugin(ChoiceFieldPlugin):
    name = _("MultipleChoice field")
    form = fields.MultipleChoiceFieldForm


class TypedMultipleChoiceFieldPlugin(ChoiceFieldPlugin):
    name = _("TypedMultipleChoice field")
    form = fields.TypedMultipleChoiceFieldForm


class ComboFieldPlugin(FormFieldPlugin):
    name = _("Combo field")
    form = fields.ComboFieldForm


class MultiValueFieldPlugin(FormFieldPlugin):
    name = _("MultiValue field")
    form = fields.MultiValueFieldForm


class FilePathFieldPlugin(ChoiceFieldPlugin):
    name = _("FilePath field")
    form = fields.FilePathFieldForm


class SplitDateTimeFieldPlugin(MultiValueFieldPlugin):
    name = _("SplitDateTime field")
    form = fields.SplitDateTimeFieldForm


class GenericIPAddressFieldPlugin(CharFieldPlugin):
    name = _("GenericIPAddress field")
    form = fields.GenericIPAddressFieldForm


class SlugFieldPlugin(CharFieldPlugin):
    name = _("Slug field")
    form = fields.SlugFieldForm


class UUIDFieldPlugin(CharFieldPlugin):
    name = _("UUID field")
    form = fields.UUIDFieldForm
