INSTALLED_APPS = [
    # ...
    "contact_form",
]

from cms_forms import config_defaults as forms_defaults  # noqa

# Add plugin to this list to have it available in the cms page editor
CMS_FORM_PLUGINS = forms_defaults.FORM_PLUGINS + ["contact_form.cms_plugins.ContactFormPlugin"]
# Or overwrite the settings to use only this plugin
CMS_FORM_PLUGINS = ["contact_form.cms_plugins.ContactFormPlugin"]
CMS_FIELD_PLUGINS = []
CMS_WIDGET_PLUGINS = []
CMS_CHOICE_OPTION_PLUGINS = []
CMS_CHOICE_FIELD_PLUGINS = []
CMS_BUTTON_PLUGINS = []
