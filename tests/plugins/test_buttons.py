from cms_forms.models import FormButton
from cms_forms.plugin_forms.buttons import BaseButtonForm
from cms_forms.plugins.buttons import BaseButtonPlugin, ButtonPlugin, SubmitButtonPlugin, ResetButtonPlugin

from tests.utils import PluginTestCase, safe_register


class CustomButtonForm(BaseButtonForm):
    input_type = "search"


class CustomButtonPlugin(BaseButtonPlugin):
    form = CustomButtonForm


class ButtonPluginTestCase(PluginTestCase):
    base_data = {
        "name": "test1",
        "value": "test2",
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        safe_register(ButtonPlugin)
        safe_register(SubmitButtonPlugin)
        safe_register(ResetButtonPlugin)
        safe_register(CustomButtonPlugin)

    def test_base_button_plugin(self):
        creation_form = BaseButtonPlugin.form(self.base_data)
        assert creation_form.is_valid()

    def test_button_plugin(self):
        plugin = self._check_plugin(
            plugin_cls=ButtonPlugin,
            plugin_model=FormButton,
            creation_data=self.base_data,
            expected_data={"input_type": "button", **self.base_data},
        )
        content = self.render_plugin_instance(ButtonPlugin, plugin)
        assert "<input" in content
        assert 'type="button' in content

    def test_submit_button_plugin(self):
        plugin = self._check_plugin(
            plugin_cls=SubmitButtonPlugin,
            plugin_model=FormButton,
            creation_data=self.base_data,
            expected_data={"input_type": "submit", **self.base_data},
        )
        content = self.render_plugin_instance(SubmitButtonPlugin, plugin)
        assert "<input" in content
        assert 'type="submit' in content

    def test_reset_button_plugin(self):
        plugin = self._check_plugin(
            plugin_cls=ResetButtonPlugin,
            plugin_model=FormButton,
            creation_data=self.base_data,
            expected_data={"input_type": "reset", **self.base_data},
        )
        content = self.render_plugin_instance(SubmitButtonPlugin, plugin)
        assert "<input" in content
        assert 'type="reset' in content
