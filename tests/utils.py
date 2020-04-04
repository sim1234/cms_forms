from cms.models import Placeholder
from cms.api import add_plugin
from cms.plugin_pool import plugin_pool
from cms.test_utils.testcases import CMSTestCase


class PluginTestCase(CMSTestCase):
    def assert_ojb_eq(self, obj, data):
        for key, value in data.items():
            self.assertEqual(getattr(obj, key), value)

    def _check_plugin(self, plugin_cls, plugin_model, creation_data, expected_data):
        plugin_cls.form()  # check empty form
        creation_form = plugin_cls.form(creation_data)  # check creation form
        assert creation_form.is_valid(), creation_form.errors
        creation_form.save()
        plugin = plugin_model.objects.get()
        self.assert_ojb_eq(plugin, expected_data)

        change_form = plugin_cls.form(instance=plugin)  # check change form
        data = {name: change_form.get_initial_for_field(field, name) for name, field in change_form.fields.items()}
        change_form = plugin_cls.form(data, instance=plugin)
        assert change_form.is_valid(), change_form.errors
        change_form.save()
        plugin = plugin_model.objects.get()
        self.assert_ojb_eq(plugin, expected_data)

        return plugin


def build_plugin(plugin, parent=None, **kwargs):
    placeholder, _ = Placeholder.objects.get_or_create(slot="test")
    return add_plugin(placeholder, plugin, "en-us", target=parent, **kwargs)


def clean_html(content: str) -> str:
    lines = [line.strip() for line in content.split("\n")]
    return "\n".join([line for line in lines if line])


def safe_register(plugin):
    if plugin.__name__ not in plugin_pool.plugins:
        plugin_pool.register_plugin(plugin)
