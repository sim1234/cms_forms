import datetime
import decimal
import uuid

from django import forms
from django.forms import fields
from django.utils.timezone import get_current_timezone

from cms_forms.importer import TypeReference
from cms_forms.models import FormField
from cms_forms.plugins.fields import (
    FormFieldPlugin,
    CharFieldPlugin,
    IntegerFieldPlugin,
    FloatFieldPlugin,
    DecimalFieldPlugin,
    BaseTemporalFieldPlugin,
    DateFieldPlugin,
    TimeFieldPlugin,
    DateTimeFieldPlugin,
    DurationFieldPlugin,
    RegexFieldPlugin,
    EmailFieldPlugin,
    FileFieldPlugin,
    ImageFieldPlugin,
    URLFieldPlugin,
    BooleanFieldPlugin,
    NullBooleanFieldPlugin,
    ChoiceFieldPlugin,
    TypedChoiceFieldPlugin,
    MultipleChoiceFieldPlugin,
    TypedMultipleChoiceFieldPlugin,
    ComboFieldPlugin,
    MultiValueFieldPlugin,
    FilePathFieldPlugin,
    SplitDateTimeFieldPlugin,
    GenericIPAddressFieldPlugin,
    SlugFieldPlugin,
    UUIDFieldPlugin,
)
from cms_forms.plugins.forms import FormPlugin

from tests.utils import build_plugin, safe_register, PluginTestCase


class FailingField(forms.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise RuntimeError("Failed to create field (xkcd-fail)")


class WidgetPluginTestCase(PluginTestCase):
    tzinfo = datetime.timezone(get_current_timezone().utcoffset(datetime.datetime(2020, 1, 1, 1, 2, 3)))

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        safe_register(FormPlugin)

        safe_register(FormFieldPlugin)
        safe_register(CharFieldPlugin)
        safe_register(IntegerFieldPlugin)
        safe_register(FloatFieldPlugin)
        safe_register(DecimalFieldPlugin)
        safe_register(BaseTemporalFieldPlugin)
        safe_register(DateFieldPlugin)
        safe_register(TimeFieldPlugin)
        safe_register(DateTimeFieldPlugin)
        safe_register(DurationFieldPlugin)
        safe_register(RegexFieldPlugin)
        safe_register(EmailFieldPlugin)
        safe_register(FileFieldPlugin)
        safe_register(ImageFieldPlugin)
        safe_register(URLFieldPlugin)
        safe_register(BooleanFieldPlugin)
        safe_register(NullBooleanFieldPlugin)
        safe_register(ChoiceFieldPlugin)
        safe_register(TypedChoiceFieldPlugin)
        safe_register(MultipleChoiceFieldPlugin)
        safe_register(TypedMultipleChoiceFieldPlugin)
        safe_register(ComboFieldPlugin)
        safe_register(MultiValueFieldPlugin)
        safe_register(FilePathFieldPlugin)
        safe_register(SplitDateTimeFieldPlugin)
        safe_register(GenericIPAddressFieldPlugin)
        safe_register(SlugFieldPlugin)
        safe_register(UUIDFieldPlugin)

    def _check_field_plugin(self, plugin_cls, field_cls, creation_data, expected_data, field_parameters=None):
        if field_parameters is None:
            field_parameters = {}
        base_data = {
            "name": "test_field",
            "field_type": TypeReference(field_cls),
            "field_parameters": {
                "disabled": False,
                "help_text": None,
                "initial": None,
                "label": None,
                "label_suffix": None,
                "localize": False,
                "required": False,
                "show_hidden_initial": False,
                **field_parameters,
            },
        }

        plugin = self._check_plugin(
            plugin_cls=plugin_cls,
            plugin_model=FormField,
            creation_data={**base_data, **creation_data},
            expected_data={**base_data, **expected_data},
        )
        field = plugin.build_field()
        assert isinstance(field, field_cls)

        content = self.render_plugin_instance(plugin_cls, plugin)
        assert content

        return plugin, field, content

    def test_widget_form(self):
        form = FormFieldPlugin.form({"name": "test"})
        form.field_type = TypeReference(FailingField)
        assert not form.is_valid(), form.errors
        assert "Failed to create field (xkcd-fail)" in form.errors["__all__"][0]

    def test_field_plugin(self):
        form = build_plugin(FormPlugin, name="test")
        field = build_plugin(
            FormFieldPlugin,
            form,
            name="field1",
            field_type=TypeReference(forms.CharField),
            field_parameters={
                "disabled": True,
                "help_text": "help",
                "initial": "5",
                "label": "lab",
                "label_suffix": "suf",
                "localize": True,
                "required": True,
                "show_hidden_initial": True,
            },
        )
        form.child_plugin_instances = [field]  # Simulate CMS tree

        form_cls = form.build_form_cls()
        frm = form_cls({"field1": "1"})
        assert isinstance(frm.fields["field1"], forms.CharField)
        assert frm.fields["field1"].disabled is True
        assert frm.fields["field1"].help_text == "help"
        assert frm.fields["field1"].initial == "5"
        assert frm.fields["field1"].label == "lab"
        assert frm.fields["field1"].label_suffix == "suf"
        assert frm.fields["field1"].localize is True
        assert frm.fields["field1"].required is True
        assert frm.fields["field1"].show_hidden_initial is True
        assert frm.is_valid(), frm.errors

        self._check_field_plugin(plugin_cls=FormFieldPlugin, field_cls=fields.Field, creation_data={}, expected_data={})

    def test_char_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=CharFieldPlugin,
            field_cls=fields.CharField,
            creation_data={"initial": "a", "empty_value": "b", "min_length": 1, "max_length": 2, "strip": True},
            expected_data={},
            field_parameters={"initial": "a", "empty_value": "b", "min_length": 1, "max_length": 2, "strip": True},
        )

    def test_integer_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=IntegerFieldPlugin,
            field_cls=fields.IntegerField,
            creation_data={"initial": 1, "min_value": 1, "max_value": 2},
            expected_data={},
            field_parameters={"initial": 1, "min_value": 1, "max_value": 2},
        )

    def test_float_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=FloatFieldPlugin,
            field_cls=fields.FloatField,
            creation_data={"initial": 1.1, "min_value": 1.1, "max_value": 2.2},
            expected_data={},
            field_parameters={"initial": 1.1, "min_value": 1.1, "max_value": 2.2},
        )

    def test_decimal_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=DecimalFieldPlugin,
            field_cls=fields.DecimalField,
            creation_data={
                "initial": "1.1",
                "min_value": "1.1",
                "max_value": "2.2",
                "decimal_places": 2,
                "max_digits": 10,
            },
            expected_data={},
            field_parameters={
                "initial": decimal.Decimal("1.1"),
                "min_value": decimal.Decimal("1.1"),
                "max_value": decimal.Decimal("2.2"),
                "decimal_places": 2,
                "max_digits": 10,
            },
        )

    def test_base_temporal_field_plugin(self):
        pass  # Just a base class

    def test_date_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=DateFieldPlugin,
            field_cls=fields.DateField,
            creation_data={"initial": "01/01/2020"},
            expected_data={},
            field_parameters={"initial": datetime.date(2020, 1, 1)},
        )

    def test_time_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=TimeFieldPlugin,
            field_cls=fields.TimeField,
            creation_data={"initial": "01:02:03"},
            expected_data={},
            field_parameters={"initial": datetime.time(1, 2, 3)},
        )

    def test_datetime_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=DateTimeFieldPlugin,
            field_cls=fields.DateTimeField,
            creation_data={"initial": "01/01/2020 01:02:03"},
            expected_data={},
            field_parameters={"initial": datetime.datetime(2020, 1, 1, 1, 2, 3, tzinfo=self.tzinfo)},
        )

    def test_duration_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=DurationFieldPlugin,
            field_cls=fields.DurationField,
            creation_data={"initial": 23},
            expected_data={},
            field_parameters={"initial": datetime.timedelta(seconds=23)},
        )

    def test_regex_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=RegexFieldPlugin,
            field_cls=fields.RegexField,
            creation_data={
                "initial": "c",
                "empty_value": "d",
                "min_length": 1,
                "max_length": 2,
                "strip": True,
                "regex": ".*",
            },
            expected_data={},
            field_parameters={
                "initial": "c",
                "empty_value": "d",
                "min_length": 1,
                "max_length": 2,
                "strip": True,
                "regex": ".*",
            },
        )

    def test_email_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=EmailFieldPlugin,
            field_cls=fields.EmailField,
            creation_data={"initial": "e@gmail.com", "empty_value": "f", "min_length": 1, "max_length": 20},
            expected_data={},
            field_parameters={"initial": "e@gmail.com", "empty_value": "f", "min_length": 1, "max_length": 20},
        )

    def test_file_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=FileFieldPlugin,
            field_cls=fields.FileField,
            creation_data={"max_length": 22, "allow_empty_file": True},
            expected_data={},
            field_parameters={"max_length": 22, "allow_empty_file": True},
        )

    def test_image_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=ImageFieldPlugin,
            field_cls=fields.ImageField,
            creation_data={"max_length": 23, "allow_empty_file": True},
            expected_data={},
            field_parameters={"max_length": 23, "allow_empty_file": True},
        )

    def test_url_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=URLFieldPlugin,
            field_cls=fields.URLField,
            creation_data={"initial": "https://gmail.com", "empty_value": "g", "min_length": 1, "max_length": 26},
            expected_data={},
            field_parameters={"initial": "https://gmail.com", "empty_value": "g", "min_length": 1, "max_length": 26},
        )

    def test_boolean_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=BooleanFieldPlugin,
            field_cls=fields.BooleanField,
            creation_data={"initial": True},
            expected_data={},
            field_parameters={"initial": True},
        )

    def test_null_boolean_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=NullBooleanFieldPlugin,
            field_cls=fields.NullBooleanField,
            creation_data={"initial": None},
            expected_data={},
            field_parameters={"initial": None},
        )

    def test_choice_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=ChoiceFieldPlugin,
            field_cls=fields.ChoiceField,
            creation_data={"initial": "h"},
            expected_data={},
            field_parameters={"initial": "h"},
        )

    def test_typed_choice_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=TypedChoiceFieldPlugin,
            field_cls=fields.TypedChoiceField,
            creation_data={"initial": "i", "empty_value": None},
            expected_data={},
            field_parameters={"initial": "i", "empty_value": None},
        )

    def test_multiple_choice_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=MultipleChoiceFieldPlugin,
            field_cls=fields.MultipleChoiceField,
            creation_data={},
            expected_data={},
            field_parameters={},
        )

    def test_typed_multiple_choice_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=TypedMultipleChoiceFieldPlugin,
            field_cls=fields.TypedMultipleChoiceField,
            creation_data={},
            expected_data={},
            field_parameters={},
        )

    def test_combo_field_plugin(self):
        pass  # TODO: implement and test this

    def test_multi_value_field_plugin(self):
        pass  # TODO: implement and test this

    def test_file_path_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=FilePathFieldPlugin,
            field_cls=fields.FilePathField,
            creation_data={
                "initial": "k",
                "path": ".",
                "match": ".*",
                "recursive": True,
                "allow_files": True,
                "allow_folders": True,
            },
            expected_data={},
            field_parameters={
                "initial": "k",
                "path": ".",
                "match": ".*",
                "recursive": True,
                "allow_files": True,
                "allow_folders": True,
            },
        )

    def test_split_datetime_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=SplitDateTimeFieldPlugin,
            field_cls=fields.SplitDateTimeField,
            creation_data={"initial": "01/01/2020 01:02:03", "require_all_fields": True},
            expected_data={},
            field_parameters={"initial": "01/01/2020 01:02:03", "require_all_fields": True},
        )

    def test_generic_ip_address_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=GenericIPAddressFieldPlugin,
            field_cls=fields.GenericIPAddressField,
            creation_data={
                "initial": "8.8.8.8",
                "protocol": "ipv4",
                "unpack_ipv4": False,
                "empty_value": "1.1.1.1",
                "min_length": 1,
                "max_length": 24,
                "strip": True,
            },
            expected_data={},
            field_parameters={
                "initial": "8.8.8.8",
                "protocol": "ipv4",
                "unpack_ipv4": False,
                "empty_value": "1.1.1.1",
                "min_length": 1,
                "max_length": 24,
                "strip": True,
            },
        )

    def test_slug_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=SlugFieldPlugin,
            field_cls=fields.SlugField,
            creation_data={
                "initial": "l",
                "empty_value": "m",
                "min_length": 1,
                "max_length": 6,
                "strip": True,
                "allow_unicode": True,
            },
            expected_data={},
            field_parameters={
                "initial": "l",
                "empty_value": "m",
                "min_length": 1,
                "max_length": 6,
                "strip": True,
                "allow_unicode": True,
            },
        )

    def test_uuid_field_plugin(self):
        self._check_field_plugin(
            plugin_cls=UUIDFieldPlugin,
            field_cls=fields.UUIDField,
            creation_data={
                "initial": "7a8b6b6f-beda-4e42-be1a-60a718285d57",
                "empty_value": "n",
                "min_length": 1,
                "max_length": 6,
                "strip": True,
            },
            expected_data={},
            field_parameters={
                "initial": uuid.UUID("7a8b6b6f-beda-4e42-be1a-60a718285d57"),
                "empty_value": "n",
                "min_length": 1,
                "max_length": 6,
                "strip": True,
            },
        )
