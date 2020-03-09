from cms.plugin_base import CMSPluginBase
from django.utils.translation import gettext_lazy as _

from ..models import Form


class BaseFormPlugin(CMSPluginBase):
    module = _("Forms")
    model = Form
    name = _("Form")
    render_template = "cms_forms/formplugin.html"
    auto_render_field_template = "cms_forms/field.html"
    allow_children = True

    def render(self, *args, **kwargs):
        context = super().render(*args, **kwargs)
        context["plugin"] = self
        return context


class FormPlugin(BaseFormPlugin):
    pass
