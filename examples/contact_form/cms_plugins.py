from django.utils.translation import gettext_lazy as _

from cms_forms.plugins.forms import FormPlugin

from .forms import ContactFormForm


# Dont register plugins manually. Use CMS_FORM_PLUGINS setting instead
class ContactFormPlugin(FormPlugin):
    form = ContactFormForm
    name = _("Contact Form")
