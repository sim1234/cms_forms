from django.db import models
from cms.models.pluginmodel import CMSPlugin

from .fields import JSONField, TypeReferenceField
from .importer import TypeReference


class Form(CMSPlugin):
    name = models.CharField(max_length=255)
    form_type = TypeReferenceField(max_length=255, default=TypeReference("django.forms.forms.Form"))

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
        form_cls = self.form_type.type
        return type("DynamicForm", (form_cls,), {field.name: field.build_field() for field in self.fields})

    def init_fields(self):
        for field in self.fields:
            field.form = self.form
            field.bound_field = self.form[field.name]


class FormField(CMSPlugin):
    name = models.CharField(max_length=255)
    field_type = TypeReferenceField(max_length=255, default=TypeReference("django.forms.fields.Field"))
    field_parameters = JSONField(default=dict, blank=True)

    form = None
    bound_field = None

    def build_field(self):
        # return fields.CharField(widget=widgets.Textarea())
        kwargs = self.field_parameters.copy()
        for plugin in self.child_plugin_instances:
            if isinstance(plugin, FormWidget):
                kwargs["widget"] = plugin.build_widget()
        return self.field_type.type(**kwargs)


class FormWidget(CMSPlugin):
    widget_type = TypeReferenceField(max_length=255, default=TypeReference("django.forms.widgets.Widget"))
    widget_parameters = JSONField(default=dict, blank=True)

    def build_widget(self):
        # return widgets.Textarea()
        return self.widget_type.type(**self.widget_parameters)
