from cms.plugin_base import CMSPluginBase
from django.utils.translation import gettext_lazy as _

from ..models import Form
from ..forms import forms


class BaseFormPlugin(CMSPluginBase):
    module = _("Forms")
    model = Form
    name = _("Form")
    render_template = "cms_forms/form.html"
    allow_children = True


class FormPlugin(BaseFormPlugin):
    pass
