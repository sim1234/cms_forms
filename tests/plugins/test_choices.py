from django import forms

from cms_forms.importer import TypeReference
from cms_forms.models import ChoiceOption
from cms_forms.plugins.choices import ChoiceOptionPlugin
from cms_forms.plugins.fields import ChoiceFieldPlugin
from cms_forms.plugins.forms import FormPlugin

from tests.utils import build_plugin, safe_register, PluginTestCase


class ChoicePluginTestCase(PluginTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        safe_register(FormPlugin)
        safe_register(ChoiceFieldPlugin)
        safe_register(ChoiceOptionPlugin)

    def test_choice_plugin(self):
        form = build_plugin(FormPlugin, name="test")
        field = build_plugin(ChoiceFieldPlugin, form, name="field1", field_type=TypeReference(forms.ChoiceField))
        form.child_plugin_instances = [field]  # Simulate CMS tree
        choice1 = build_plugin(ChoiceOptionPlugin, form, value="1", display="One")
        choice2 = build_plugin(ChoiceOptionPlugin, form, value="2", display="Two")
        field.child_plugin_instances = [choice1, choice2]  # Simulate CMS tree

        choices = list(ChoiceOption.objects.values_list("value", "display"))
        assert choices == [("1", "One"), ("2", "Two")]

        form_cls = form.build_form_cls()
        frm = form_cls({"field1": "1"})
        assert frm.fields["field1"].choices == choices
        assert frm.is_valid(), frm.errors
        frm = form_cls({"field1": "3"})
        assert not frm.is_valid(), frm.errors

        plugin = self._check_plugin(
            plugin_cls=ChoiceOptionPlugin,
            plugin_model=ChoiceOption,
            creation_data={"value": "1", "display": "One"},
            expected_data={"value": "1", "display": "One"},
        )
        content = self.render_plugin_instance(ChoiceOptionPlugin, plugin)
        assert content == ""
