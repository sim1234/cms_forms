from cms_forms.importer import TypeReference, Importer


class MyClass:
    pass


def test_importer():
    v_str = Importer.to_string(MyClass)
    v_cls = Importer.from_string(v_str)
    assert isinstance(v_str, str)
    assert v_cls is MyClass
    assert Importer.to_string(TypeReference) == "cms_forms.importer.TypeReference"
    assert Importer.from_string("cms_forms.importer.TypeReference") is TypeReference
    tr = TypeReference(TypeReference)
    assert Importer.to_string(tr) == "cms_forms.importer.TypeReference"
    assert Importer.from_string(tr) is TypeReference


def test_type_reference():
    tr1 = TypeReference(MyClass)
    tr2 = TypeReference(tr1)
    assert tr1 == tr2
    assert tr1.str == tr2.str
    assert tr1.type is MyClass
    assert tr2.type is MyClass
    tr3 = TypeReference(TypeReference)
    tr4 = TypeReference("cms_forms.importer.TypeReference")
    assert tr3 == tr4
    assert tr3.str == tr4.str == "cms_forms.importer.TypeReference"
    assert tr3.type is TypeReference
    assert tr4.type is TypeReference
    assert str(tr3) == "cms_forms.importer.TypeReference"
    assert tr1 != tr3
    assert tr1 != None  # noqa
    assert repr(tr1)
    assert len(tr1)
    assert tr3.deconstruct() == ("cms_forms.importer.TypeReference", ["cms_forms.importer.TypeReference"], {})
