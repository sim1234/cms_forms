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
        raise RuntimeError("Failed to create form (xkcd-fail)")


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
                "form_type": TypeReference(form_cls),  # not always set but checked
                "meta_parameters": {},  # not always set but checked
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

        content = self.render_plugin_instance(plugin_cls, plugin)
        assert "<form" in content

        return plugin, frm, content

    def test_form_form(self):
        form = BaseFormPlugin.form({"name": "test", "load": LoadEnum.RELOAD.name, "auto_render_fields": True})
        form.form_type = TypeReference(FailingForm)
        assert not form.is_valid(), form.errors
        assert "Failed to create form (xkcd-fail)" in form.errors["__all__"][0]

    def test_form_plugin(self):
        self._check_form_plugin(
            plugin_cls=FormPlugin, form_cls=forms.Form, creation_data={}, expected_data={},
        )

    def test_model_form_plugin(self):
        # Using ChoiceOption model as it already exists in the database
        _, _, content = self._check_form_plugin(
            plugin_cls=ModelFormPlugin,
            form_cls=forms.ModelForm,
            creation_data={"model": TypeReference(ChoiceOption).str, "fields": "__all__", "exclude": None},
            expected_data={"meta_parameters": {"model": ChoiceOption, "fields": "__all__", "exclude": None}},
        )
        assert 'name="value"' in content
        assert 'name="display"' in content

        _, _, content = self._check_form_plugin(
            plugin_cls=ModelFormPlugin,
            form_cls=forms.ModelForm,
            creation_data={"model": TypeReference(ChoiceOption).str, "fields": None, "exclude": "value"},
            expected_data={"meta_parameters": {"model": ChoiceOption, "fields": None, "exclude": ["value"]}},
        )
        assert 'name="value"' not in content
        assert 'name="display"' in content

    def test_custom_plugin(self):
        plugin, _, content = self._check_form_plugin(
            plugin_cls=MyFormPlugin,
            form_cls=MyForm,
            creation_data={"extra_field": "test2"},
            expected_data={"meta_parameters": {"extra_field": "test2"}},
            form_data={"field1": "test3"},
        )
        assert 'name="field1"' in content

        plugin.load = LoadEnum.STATIC.name
        plugin.save()
        content = self.render_plugin_instance(MyFormPlugin, plugin)
        assert 'name="field1"' in content

        plugin.load = LoadEnum.LAZY.name
        plugin.save()
        content = self.render_plugin_instance(MyFormPlugin, plugin)
        assert 'name="field1"' not in content
