from django.conf import settings

from . import defaults


def name(s):
    return s.split(".")[-1]


def configure(key):
    return getattr(settings, f"CMS_{key}", getattr(defaults, key))


FORM_PLUGINS = configure("FORM_PLUGINS")
FIELD_PLUGINS = configure("FIELD_PLUGINS")
WIDGET_PLUGINS = configure("WIDGET_PLUGINS")
CHOICE_OPTION_PLUGINS = configure("CHOICE_OPTION_PLUGINS")
CHOICE_FIELD_PLUGINS = configure("CHOICE_FIELD_PLUGINS")
BUTTON_PLUGINS = configure("BUTTON_PLUGINS")

FORM_PLUGIN_NAMES = [name(p) for p in FORM_PLUGINS]
FIELD_PLUGIN_NAMES = [name(p) for p in FIELD_PLUGINS]
WIDGET_PLUGIN_NAMES = [name(p) for p in WIDGET_PLUGINS]
CHOICE_OPTION_PLUGIN_NAMES = [name(p) for p in CHOICE_OPTION_PLUGINS]
CHOICE_FIELD_PLUGIN_NAMES = [name(p) for p in CHOICE_FIELD_PLUGINS]
BUTTON_PLUGIN_NAMES = [name(p) for p in BUTTON_PLUGINS]
