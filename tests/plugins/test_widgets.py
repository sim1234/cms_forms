from django import forms
from django.forms import widgets

from cms_forms.importer import TypeReference
from cms_forms.models import FormWidget
from cms_forms.plugins.widgets import (
    WidgetPlugin,
    InputPlugin,
    TextInputPlugin,
    NumberInputPlugin,
    EmailInputPlugin,
    URLInputPlugin,
    PasswordInputPlugin,
    HiddenInputPlugin,
    MultipleHiddenInputPlugin,
    FileInputPlugin,
    ClearableFileInputPlugin,
    TextareaPlugin,
    DateTimeBaseInput,
    DateInputPlugin,
    DateTimeInputPlugin,
    TimeInputPlugin,
    CheckboxInputPlugin,
    ChoiceWidgetPlugin,
    SelectPlugin,
    NullBooleanSelectPlugin,
    SelectMultiplePlugin,
    CheckboxSelectMultiplePlugin,
    MultiWidgetPlugin,
    SplitDateTimeWidgetPlugin,
    SplitHiddenDateTimeWidgetPlugin,
    SelectDateWidgetPlugin,
)
from cms_forms.plugins.fields import FormFieldPlugin
from cms_forms.plugins.forms import FormPlugin

from tests.utils import build_plugin, safe_register, PluginTestCase


class WidgetPluginTestCase(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        safe_register(FormPlugin)
        safe_register(FormFieldPlugin)

        safe_register(WidgetPlugin)
        safe_register(InputPlugin)
        safe_register(TextInputPlugin)
        safe_register(NumberInputPlugin)
        safe_register(EmailInputPlugin)
        safe_register(URLInputPlugin)
        safe_register(PasswordInputPlugin)
        safe_register(HiddenInputPlugin)
        safe_register(MultipleHiddenInputPlugin)
        safe_register(FileInputPlugin)
        safe_register(ClearableFileInputPlugin)
        safe_register(TextareaPlugin)
        safe_register(DateTimeBaseInput)
        safe_register(DateInputPlugin)
        safe_register(DateTimeInputPlugin)
        safe_register(TimeInputPlugin)
        safe_register(CheckboxInputPlugin)
        safe_register(ChoiceWidgetPlugin)
        safe_register(SelectPlugin)
        safe_register(NullBooleanSelectPlugin)
        safe_register(SelectMultiplePlugin)
        safe_register(CheckboxSelectMultiplePlugin)
        safe_register(MultiWidgetPlugin)
        safe_register(SplitDateTimeWidgetPlugin)
        safe_register(SplitHiddenDateTimeWidgetPlugin)
        safe_register(SelectDateWidgetPlugin)

    def _check_widget_plugin(self, plugin_cls, widget_cls, creation_data, expected_data, widget_parameters=None):
        if widget_parameters is None:
            widget_parameters = {"attrs": None}
        base_data = {"widget_type": TypeReference(widget_cls), "widget_parameters": widget_parameters}

        plugin = self._check_plugin(
            plugin_cls=plugin_cls,
            plugin_model=FormWidget,
            creation_data={**base_data, **creation_data},
            expected_data={**base_data, **expected_data},
        )
        widget = plugin.build_widget()
        assert isinstance(widget, widget_cls)

        content = self.render_plugin_instance(plugin_cls, plugin)
        assert content == ""

        return plugin, widget

    def test_widget_plugin(self):
        form = build_plugin(FormPlugin, name="test")
        field = build_plugin(FormFieldPlugin, form, name="field1", field_type=TypeReference(forms.CharField))
        form.child_plugin_instances = [field]  # Simulate CMS tree
        widget = build_plugin(WidgetPlugin, form, widget_type=TypeReference(widgets.Textarea))
        field.child_plugin_instances = [widget]  # Simulate CMS tree

        form_cls = form.build_form_cls()
        frm = form_cls({"field1": "1"})
        assert isinstance(frm.fields["field1"].widget, forms.Textarea)
        assert frm.is_valid(), frm.errors

        self._check_widget_plugin(
            plugin_cls=WidgetPlugin, widget_cls=widgets.Widget, creation_data={}, expected_data={}
        )

    def test_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=InputPlugin,
            widget_cls=widgets.Input,
            creation_data={"type": "custom"},
            expected_data={},
            widget_parameters={"attrs": {"type": "custom"}},
        )

    def test_text_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=TextInputPlugin, widget_cls=widgets.TextInput, creation_data={}, expected_data={}
        )

    def test_number_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=NumberInputPlugin, widget_cls=widgets.NumberInput, creation_data={}, expected_data={}
        )

    def test_email_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=EmailInputPlugin, widget_cls=widgets.EmailInput, creation_data={}, expected_data={}
        )

    def test_url_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=URLInputPlugin, widget_cls=widgets.URLInput, creation_data={}, expected_data={}
        )

    def test_password_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=PasswordInputPlugin,
            widget_cls=widgets.PasswordInput,
            creation_data={"render_value": True},
            expected_data={},
            widget_parameters={"attrs": None, "render_value": True},
        )

    def test_hidden_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=HiddenInputPlugin, widget_cls=widgets.HiddenInput, creation_data={}, expected_data={}
        )

    def test_multipleHidden_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=MultipleHiddenInputPlugin,
            widget_cls=widgets.MultipleHiddenInput,
            creation_data={},
            expected_data={},
        )

    def test_file_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=FileInputPlugin, widget_cls=widgets.FileInput, creation_data={}, expected_data={}
        )

    def test_clearable_file_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=ClearableFileInputPlugin,
            widget_cls=widgets.ClearableFileInput,
            creation_data={},
            expected_data={},
        )

    def test_textarea_plugin(self):
        self._check_widget_plugin(
            plugin_cls=TextareaPlugin,
            widget_cls=widgets.Textarea,
            creation_data={"cols": 10, "rows": 20},
            expected_data={},
            widget_parameters={"attrs": {"cols": 10, "rows": 20}},
        )

    def test_datetime_base_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=DateTimeBaseInput,
            widget_cls=widgets.DateTimeBaseInput,
            creation_data={"format": "%s"},
            expected_data={},
            widget_parameters={"attrs": None, "format": "%s"},
        )

    def test_date_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=DateInputPlugin,
            widget_cls=widgets.DateInput,
            creation_data={"format": "%s"},
            expected_data={},
            widget_parameters={"attrs": None, "format": "%s"},
        )

    def test_datetime_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=DateTimeInputPlugin,
            widget_cls=widgets.DateTimeInput,
            creation_data={"format": "%s"},
            expected_data={},
            widget_parameters={"attrs": None, "format": "%s"},
        )

    def test_time_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=TimeInputPlugin,
            widget_cls=widgets.TimeInput,
            creation_data={"format": "%s"},
            expected_data={},
            widget_parameters={"attrs": None, "format": "%s"},
        )

    def test_checkbox_input_plugin(self):
        self._check_widget_plugin(
            plugin_cls=CheckboxInputPlugin, widget_cls=widgets.CheckboxInput, creation_data={}, expected_data={}
        )

    def test_choice_widget_plugin(self):
        self._check_widget_plugin(
            plugin_cls=ChoiceWidgetPlugin, widget_cls=widgets.ChoiceWidget, creation_data={}, expected_data={}
        )

    def test_select_plugin(self):
        self._check_widget_plugin(
            plugin_cls=SelectPlugin, widget_cls=widgets.Select, creation_data={}, expected_data={}
        )

    def test_null_boolean_select_plugin(self):
        self._check_widget_plugin(
            plugin_cls=NullBooleanSelectPlugin, widget_cls=widgets.NullBooleanSelect, creation_data={}, expected_data={}
        )

    def test_select_multiple_plugin(self):
        self._check_widget_plugin(
            plugin_cls=SelectMultiplePlugin, widget_cls=widgets.SelectMultiple, creation_data={}, expected_data={}
        )

    def test_checkbox_select_multiple_plugin(self):
        self._check_widget_plugin(
            plugin_cls=CheckboxSelectMultiplePlugin,
            widget_cls=widgets.CheckboxSelectMultiple,
            creation_data={},
            expected_data={},
        )

    def test_multi_widget_plugin(self):
        pass  # TODO: implement and test this

    def test_split_datetime_widget_plugin(self):
        self._check_widget_plugin(
            plugin_cls=SplitDateTimeWidgetPlugin,
            widget_cls=widgets.SplitDateTimeWidget,
            creation_data={"date_format": "%s", "time_format": "%s", "date_attrs": None, "time_attrs": None,},
            expected_data={},
            widget_parameters={
                "attrs": None,
                "date_format": "%s",
                "time_format": "%s",
                "date_attrs": None,
                "time_attrs": None,
            },
        )

    def test_split_hidden_datetime_widget_plugin(self):
        self._check_widget_plugin(
            plugin_cls=SplitHiddenDateTimeWidgetPlugin,
            widget_cls=widgets.SplitHiddenDateTimeWidget,
            creation_data={"date_format": "%s", "time_format": "%s", "date_attrs": None, "time_attrs": None,},
            expected_data={},
            widget_parameters={
                "attrs": None,
                "date_format": "%s",
                "time_format": "%s",
                "date_attrs": None,
                "time_attrs": None,
            },
        )

    def test_select_date_widget_plugin(self):
        self._check_widget_plugin(
            plugin_cls=SelectDateWidgetPlugin,
            widget_cls=widgets.SelectDateWidget,
            creation_data={"years": [2020], "months": [1, 2], "empty_label": "test"},
            expected_data={},
            widget_parameters={"attrs": None, "years": [2020], "months": [1, 2], "empty_label": "test",},
        )
