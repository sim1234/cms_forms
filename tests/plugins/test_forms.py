from django import forms

from cms_forms.importer import TypeReference
from cms_forms.models import Form, ChoiceOption
from cms_forms.enums import LoadEnum
from cms_forms.plugin_forms.forms import BaseModelFormForm
from cms_forms.plugins.forms import BaseFormPlugin, FormPlugin, ModelFormPlugin, SavingFormPlugin

from tests.utils import PluginTestCase, safe_register


class MyForm(forms.Form):
    field1 = forms.CharField()


class MyFormForm(BaseModelFormForm):
    form_type = TypeReference(MyForm)
    meta_parameters = ["extra_field"]

    extra_field = forms.CharField()


class MyFormPlugin(BaseFormPlugin):
    form = MyFormForm


class FailingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise RuntimeError("Failed to create form")


class FormPluginTestCase(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        safe_register(FormPlugin)
        safe_register(ModelFormPlugin)
        safe_register(SavingFormPlugin)
        safe_register(MyFormPlugin)

    def _check_form_plugin(self, plugin_cls, form_cls, creation_data, expected_data, form_data=None, base_data=None):
        if form_data is None:
            form_data = {}
        if base_data is None:
            base_data = {
                "name": "test",
                "load": LoadEnum.RELOAD.name,
                "auto_render_fields": True,
                "form_type": TypeReference(form_cls),
                "meta_parameters": {},
            }

        plugin = self._check_plugin(
            plugin_cls=plugin_cls,
            plugin_model=Form,
            creation_data={**base_data, **creation_data},
            expected_data={**base_data, **expected_data},
        )

        frm = plugin.build_form_cls()(form_data)
        assert isinstance(frm, form_cls)
        assert frm.is_valid(), frm.errors

        return plugin, frm

    def test_base_form_plugin(self):
        creation_form = BaseFormPlugin.form(
            {
                "name": "test",
                "load": LoadEnum.RELOAD.name,
                "auto_render_fields": True,
                "form_type": TypeReference(FailingForm),
            }
        )
        assert not creation_form.is_valid()

    def test_form_plugin(self):
        self._check_form_plugin(
            plugin_cls=FormPlugin, form_cls=forms.Form, creation_data={}, expected_data={},
        )

    def test_model_form_plugin(self):
        # Using ChoiceOption model as it already exists in the database
        self._check_form_plugin(
            plugin_cls=ModelFormPlugin,
            form_cls=forms.ModelForm,
            creation_data={"model": TypeReference(ChoiceOption).str, "fields": "__all__", "exclude": None},
            expected_data={"meta_parameters": {"model": ChoiceOption, "fields": "__all__", "exclude": None}},
        )
        Form.objects.all().delete()
        self._check_form_plugin(
            plugin_cls=ModelFormPlugin,
            form_cls=forms.ModelForm,
            creation_data={"model": TypeReference(ChoiceOption).str, "fields": None, "exclude": "value"},
            expected_data={"meta_parameters": {"model": ChoiceOption, "fields": None, "exclude": ["value"]}},
        )

    def test_custom_plugin(self):
        self._check_form_plugin(
            plugin_cls=MyFormPlugin,
            form_cls=MyForm,
            creation_data={"extra_field": "test2"},
            expected_data={"meta_parameters": {"extra_field": "test2"}},
            form_data={"field1": "test3"},
        )
