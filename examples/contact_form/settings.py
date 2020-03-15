from cms_forms import defaults as forms_defaults  # noqa

INSTALLED_APPS = [
    # ...
    "contact_form",
]

CMS_FORM_PLUGINS = forms_defaults.FORM_PLUGINS + ["contact_form.cms_plugins.ContactFormPlugin"]
