from cms.test_utils.testcases import CMSTestCase
from django import forms
from django.core.files.base import ContentFile
from django.forms import widgets

from cms_forms.importer import TypeReference
from cms_forms.models import Form, FormField, FormWidget, ChoiceOption, FormButton, FormSubmission, FormSubmissionFile
from cms_forms.enums import LoadEnum


class MyForm(forms.Form):
    pass


class MyField(forms.Field):
    pass


class MyWidget(widgets.Widget):
    pass


def build_form(child_plugins=None, **kwargs) -> Form:
    data = {
        "name": "test",
        "form_type": TypeReference(MyForm),
        "meta_parameters": {},
        "auto_render_fields": False,
        "load": LoadEnum.RELOAD.name,
    }
    data.update(kwargs)
    obj = Form.objects.create(**data)
    if child_plugins:
        obj.child_plugin_instances = child_plugins
    return obj


def build_form_field(child_plugins=None, **kwargs) -> FormField:
    data = {
        "name": "test",
        "field_type": TypeReference(MyField),
        "field_parameters": {},
    }
    data.update(kwargs)
    obj = FormField.objects.create(**data)
    if child_plugins:
        obj.child_plugin_instances = child_plugins
    return obj


def build_widget(**kwargs) -> FormWidget:
    data = {
        "widget_type": TypeReference(MyWidget),
        "widget_parameters": {},
    }
    data.update(kwargs)
    return FormWidget.objects.create(**data)


def build_button(**kwargs):
    data = {
        "input_type": "submit",
        "name": "test",
        "value": "Test",
    }
    data.update(kwargs)
    return FormButton.objects.create(**data)


def build_choice(value="test", display="test"):
    return ChoiceOption.objects.create(value=value, display=display)


class ModelsTestCase(CMSTestCase):
    def test_form_methods(self):
        form = build_form()
        form_cls = form.build_form_cls()
        assert issubclass(form_cls, MyForm)
        assert isinstance(form.form, MyForm)
        assert len(form.fields) == 0
        assert len(form.form.fields) == 0
        new_form = form_cls({})
        form.form = new_form
        assert form.form is new_form
        assert not form.is_lazy
        assert not form.is_static
        assert not form.get_child_plugin_instances()
        assert form.form.is_valid(), form.form.errors
        assert isinstance(form.__str__(), str)

    def test_field_methods(self):
        field = build_form_field()
        field_instance = field.build_field()
        assert isinstance(field_instance, MyField)
        assert isinstance(field.__str__(), str)

    def test_widget_methods(self):
        widget = build_widget()
        widget_instance = widget.build_widget()
        assert isinstance(widget_instance, MyWidget)
        assert isinstance(widget.__str__(), str)

    def test_button_methods(self):
        button = build_button()
        value = button.render_button()
        assert value.startswith("<input")
        assert 'type="submit"' in value
        assert 'name="test"' in value
        assert 'value="Test"' in value
        assert isinstance(button.__str__(), str)

    def test_choice_methods(self):
        choice = build_choice("test", "Test")
        assert isinstance(choice.__str__(), str)

    def test_submission_methods(self):
        submission = FormSubmission.objects.create(form_name="test", data={})
        submission_file = FormSubmissionFile.objects.create(
            submission=submission, field_name="test", file=ContentFile("test")
        )
        assert isinstance(submission.__str__(), str)
        assert isinstance(submission_file.__str__(), str)

    def test_form_with_fields(self):
        field1 = build_form_field(name="test1")
        field2 = build_form_field(name="test2")
        other_plugin = Form("test3")
        form = build_form(child_plugins=[field1, field2, other_plugin])
        assert form.get_child_plugin_instances() == [field1, field2, other_plugin]  # build form
        assert form.fields == [field1, field2]
        assert field1.form is form.form
        assert field2.form is form.form
        assert isinstance(field1.bound_field, forms.BoundField)
        assert isinstance(field2.bound_field, forms.BoundField)
        assert field1.bound_field.name == "test1"
        assert field2.bound_field.name == "test2"
        assert field1.bound_field.value() is None
        assert field2.bound_field.value() is None

    def test_form_with_fields_initial_form(self):
        field1 = build_form_field(name="test1")
        field2 = build_form_field(name="test2")
        form = build_form(child_plugins=[field1, field2])
        new_form = form.build_form_cls()({"test1": "a", "test2": "b"})
        form.form = new_form
        assert form.get_child_plugin_instances() == [field1, field2]  # build form
        assert form.form.is_valid(), form.form.errors
        assert field1.form is new_form
        assert field2.form is new_form
        assert field1.bound_field.value() == "a"
        assert field2.bound_field.value() == "b"

    def test_field_with_widget(self):
        widget = build_widget()
        field = build_form_field(child_plugins=[widget])
        form = build_form(child_plugins=[field])
        assert form.get_child_plugin_instances() == [field]  # build form
        assert isinstance(field.bound_field.field.widget, MyWidget)

    def test_field_with_choices(self):
        choice1 = build_choice("test1", "T")
        choice2 = build_choice("test2", "TT")
        field = build_form_field(child_plugins=[choice1, choice2], field_type=TypeReference(forms.ChoiceField))
        form = build_form(child_plugins=[field])
        assert form.get_child_plugin_instances() == [field]  # build form
        assert field.bound_field.field.choices == [("test1", "T"), ("test2", "TT")]

    def test_field_with_choices_not_breaks(self):
        choice = build_choice("test1", "T")
        field = build_form_field(child_plugins=[choice])
        form = build_form(child_plugins=[field])
        assert form.get_child_plugin_instances() == [field]  # build form
        assert field.bound_field
