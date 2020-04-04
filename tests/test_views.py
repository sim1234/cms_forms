import pytest

from cms.models import Page
from cms.test_utils.testcases import CMSTestCase
from django import forms
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.test import RequestFactory

from cms_forms.forms import BaseForm
from cms_forms.importer import TypeReference
from cms_forms.plugins.forms import FormPlugin
from cms_forms.plugins.fields import FormFieldPlugin
from cms_forms.views import get_plugin, render_plugin, BaseFormSubmissionView
from cms_forms.models import Form

from tests.utils import safe_register, build_plugin, clean_html


class RedirectingForm(BaseForm):
    def cms_save(self, request, plugin):
        return redirect("/success/")


class SuccessForm(BaseForm):
    field1 = forms.IntegerField()

    def cms_save(self, request, plugin):
        return HttpResponse("Success!")


class ViewsTestCase(CMSTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        safe_register(FormPlugin)
        safe_register(FormFieldPlugin)

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def cms_request(self, method="get", **kwargs):
        request = getattr(self.factory, method)("/", **kwargs)
        request.current_page = Page()
        return request

    def test_get_plugin(self):
        form = build_plugin(FormPlugin, name="test")
        form2 = Form.objects.create(name="test2")
        assert get_plugin(None, Form, form.pk) == form
        with pytest.raises(Http404):
            get_plugin(self.cms_request(), Form, form2.pk + 1)
        with pytest.raises(Http404):
            get_plugin(self.cms_request(), Form, form2.pk)

    def test_render_plugin(self):
        form = build_plugin(FormPlugin, name="test")
        content = render_plugin(self.cms_request(), form)
        assert "<form" in content

    def test_submission_view(self):
        form = build_plugin(FormPlugin, name="test")
        build_plugin(FormFieldPlugin, form, name="field1")
        build_plugin(FormFieldPlugin, form, name="field2")
        view = BaseFormSubmissionView.as_view(model=Form)

        # Get rendering
        response = view(self.cms_request(), form_pk=form.pk)
        content = clean_html(response.content.decode("utf-8"))
        assert response.status_code == 200
        assert "<form" not in content
        assert "<input" in content
        assert 'id="id_field1"' in content
        assert 'name="field1"' in content
        assert 'name="field2"' in content

        # Post processing and rendering
        response = view(self.cms_request("post", data={"field1": "data1", "field2": "data2"}), form_pk=form.pk)
        content = clean_html(response.content.decode("utf-8"))
        assert response.status_code == 200
        assert "<form" not in content
        assert "<input" in content
        assert 'id="id_field1"' in content
        assert 'name="field1"' in content
        assert 'name="field2"' in content
        assert 'value="data1"' in content
        assert 'value="data1"' in content

    def test_submission_view_custom_form(self):
        # redirect response
        form = build_plugin(FormPlugin, name="test", form_type=TypeReference(RedirectingForm))
        view = BaseFormSubmissionView.as_view(model=Form)
        response = view(self.cms_request("post", data={}), form_pk=form.pk)
        assert response.status_code == 302
        assert response.url == "/success/"

        # form not valid
        form = build_plugin(FormPlugin, name="test", form_type=TypeReference(SuccessForm), auto_render_fields=True)
        response = view(self.cms_request("post", data={}), form_pk=form.pk)
        content = clean_html(response.content.decode("utf-8"))
        assert response.status_code == 200
        assert "<input" in content

        # plain response
        response = view(self.cms_request("post", data={"field1": 1}), form_pk=form.pk)
        content = clean_html(response.content.decode("utf-8"))
        assert response.status_code == 200
        assert content == "Success!"
