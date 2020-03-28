import pytest

from django.core.exceptions import ValidationError

from cms_forms.fields import JSONField, JSONFormField, TypeReferenceField, TypeReferenceFormField
from cms_forms.importer import TypeReference


def test_json_field():
    field = JSONField(default=dict, null=True)
    assert field.from_db_value(None) is None
    assert field.from_db_value('{"a": 1}') == {"a": 1}
    assert field.from_db_value('"test"') == "test"
    assert field.from_db_value({"a": 1}) == {"a": 1}
    assert field.value_to_string(None) == "null"
    assert field.value_to_string({"a": 1}) == '{"a": 1}'
    assert isinstance(field.formfield(), JSONFormField)
    with pytest.raises(ValidationError):
        field.from_db_value("broken:json")


def test_json_form_field():
    field = JSONFormField(required=False)
    assert field.to_python(None) is None
    assert field.to_python("") is None
    assert field.to_python('{"a": 1}') == {"a": 1}
    assert field.to_python('"test"') == "test"
    assert field.prepare_value(None) == "null"
    assert field.prepare_value({"a": 1}) == '{"a": 1}'
    with pytest.raises(ValidationError):
        field.to_python("broken:json")


def test_type_reference_field():
    tr = TypeReference(TypeReference)
    field = TypeReferenceField(default=tr, null=True)
    assert field.from_db_value(None) is None
    assert field.from_db_value("cms_forms.importer.TypeReference").str == "cms_forms.importer.TypeReference"
    assert field.from_db_value(tr).str == "cms_forms.importer.TypeReference"
    assert field.value_to_string(None) is None
    assert field.value_to_string("cms_forms.importer.TypeReference") == "cms_forms.importer.TypeReference"
    assert field.value_to_string(tr) == "cms_forms.importer.TypeReference"
    assert isinstance(field.formfield(), TypeReferenceFormField)
    with pytest.raises(ValidationError):
        field.from_db_value("test.BrokenPath")


def test_type_reference_form_field():
    tr = TypeReference(TypeReference)
    field = TypeReferenceFormField(required=False)
    assert field.to_python(None) is None
    assert field.to_python("") is None
    assert field.to_python("cms_forms.importer.TypeReference").str == "cms_forms.importer.TypeReference"
    assert field.to_python(tr).str == "cms_forms.importer.TypeReference"
    assert field.prepare_value(None) is None
    assert field.prepare_value("cms_forms.importer.TypeReference") == "cms_forms.importer.TypeReference"
    assert field.prepare_value(tr) == "cms_forms.importer.TypeReference"
    with pytest.raises(ValidationError):
        field.to_python("test.BrokenPath")
