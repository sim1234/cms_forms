from cms.models import Placeholder, Page
from cms.api import add_plugin
from cms.plugin_pool import plugin_pool
from cms.test_utils.testcases import CMSTestCase
from django.test import RequestFactory

from cms_forms.views import render_plugin


class PluginTestCase(CMSTestCase):
    factory = RequestFactory()

    def cms_request(self, method="get", **kwargs):
        request = getattr(self.factory, method)("/", **kwargs)
        request.current_page = Page()
        return request

    def render_plugin_instance(self, plugin_cls, plugin):
        model = type(plugin)
        values = dict(model.objects.filter(pk=plugin.pk).values()[0])
        for key in [
            "id",
            "depth",
            "numchild",
            "language",
            "position",
            "creation_date",
            "changed_date",
            "plugin_type",
            "path",
            "cmsplugin_ptr_id",
        ]:
            values.pop(key, None)
        plugin = build_plugin(plugin_cls, **values)
        return render_plugin(self.cms_request(), plugin)

    def assert_ojb_eq(self, obj, data):
        for key, value in data.items():
            self.assertEqual(getattr(obj, key), value)

    def _check_plugin(self, plugin_cls, plugin_model, creation_data, expected_data):
        plugin_cls.form()  # check empty form
        creation_form = plugin_cls.form(creation_data)  # check creation form
        assert creation_form.is_valid(), creation_form.errors
        creation_form.save()
        plugin = plugin_model.objects.get(pk=creation_form.instance.pk)
        self.assert_ojb_eq(plugin, expected_data)

        change_form = plugin_cls.form(instance=plugin)  # check change form
        data = {name: change_form.get_initial_for_field(field, name) for name, field in change_form.fields.items()}
        change_form = plugin_cls.form(data, instance=plugin)
        assert change_form.is_valid(), change_form.errors
        change_form.save()
        plugin = plugin_model.objects.get(pk=change_form.instance.pk)
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
