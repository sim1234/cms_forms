import json

from django.db import models
from cms.models.pluginmodel import CMSPlugin
from django.forms import forms, fields, widgets
from django.core import validators
from django.utils.translation import gettext_lazy as _

from .json import CustomJSONEncoder, CustomJSONDecoder

FIELD_TYPE_CHOICES = (
    ("", _("")),
)
WIDGET_CHOICES = (
    (None, _("Default")),
)


class Form(CMSPlugin):
    name = models.CharField(max_length=255)

    _fields = None
    _form = None
    render_inner_only = False

    @property
    def fields(self):
        if self._fields is None:
            self._fields = list(self.get_form_fields(self))
        return self._fields

    @property
    def form(self):
        if self._form is None:
            self._form = self.build_form_cls()()
        return self._form

    @form.setter
    def form(self, value):
        self._form = value

    @classmethod
    def get_form_fields(cls, plugin):
        for plugin in plugin.child_plugin_instances:
            if isinstance(plugin, FormField):
                yield plugin
            else:
                yield from cls.get_form_fields(plugin)

    def get_child_plugin_instances(self):  # rendering hook
        self.init_fields()
        return self.child_plugin_instances

    def build_form_cls(self):
        return type("DynamicForm", (forms.Form,), {field.name: field.build_field() for field in self.fields})

    def init_fields(self):
        for field in self.fields:
            field.form = self.form
            field.bound_field = self.form[field.name]


class FormField(CMSPlugin):
    name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=255)
    field_parameters = models.TextField(default="{}")
    widget_type = models.CharField(max_length=255, blank=True, default="")
    widget_parameters = models.TextField(default="{}")

    form = None
    bound_field = None

    @property
    def kwargs(self):
        return json.loads(self.field_parameters, cls=CustomJSONDecoder)

    @kwargs.setter
    def kwargs(self, value):
        self.field_parameters = json.dumps(value, cls=CustomJSONEncoder)

    @property
    def widget_kwargs(self):
        return json.loads(self.widget_parameters, cls=CustomJSONDecoder)

    @widget_kwargs.setter
    def widget_kwargs(self, value):
        self.widget_parameters = json.dumps(value, cls=CustomJSONEncoder)

    def build_field(self):
        # return fields.CharField(widget=widgets.Textarea())
        kwargs = self.kwargs
        if self.widget_type:
            widget_cls = getattr(widgets, self.widget_type)
            kwargs["widget"] = widget_cls(**self.widget_kwargs)
        field_cls = getattr(fields, self.field_type)
        return field_cls(**kwargs)
