from cms.test_utils.testcases import CMSTestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from cms_forms.forms import SavingForm, BaseForm
from cms_forms.importer import TypeReference
from cms_forms.models import FormSubmission, FormSubmissionFile
from cms_forms.plugins.fields import FormFieldPlugin
from cms_forms.plugins.forms import FormPlugin

from tests.test_views import build_plugin, safe_register


class MyForm(BaseForm):
    saved = False

    def save(self):
        self.saved = True


class FormsTestCase(CMSTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        safe_register(FormPlugin)
        safe_register(FormFieldPlugin)

    def test_saving_form(self):
        form = build_plugin(
            FormPlugin, name="test", form_type=TypeReference(SavingForm), meta_parameters={"success_content": "Yay"}
        )
        field = build_plugin(FormFieldPlugin, form, name="field1")
        form.child_plugin_instances = [field]  # Simulate CMS tree

        frm = form.build_form_cls()({"field1": "test1", "other": "stuff"})
        assert isinstance(frm, SavingForm)
        assert frm.is_valid()
        response = frm.cms_save(None, form)
        submission = FormSubmission.objects.get()
        assert submission.form_name == "test"
        assert submission.data == {"field1": "test1"}
        assert response.status_code == 200
        assert response.content == b"Yay"

    def test_saving_form_files(self):
        form = build_plugin(
            FormPlugin, name="test", form_type=TypeReference(SavingForm), meta_parameters={"success_url": "/thank-you/"}
        )
        field1 = build_plugin(FormFieldPlugin, form, name="field1")
        field2 = build_plugin(
            FormFieldPlugin, form, name="field2", field_type=TypeReference("django.forms.fields.FileField")
        )
        form.child_plugin_instances = [field1, field2]  # Simulate CMS tree

        frm = form.build_form_cls()({"field1": "test1"}, {"field2": SimpleUploadedFile("text.txt", b"content")})
        assert isinstance(frm, SavingForm)
        assert frm.is_valid(), frm.errors
        response = frm.cms_save(None, form)
        submission = FormSubmission.objects.get()
        assert submission.form_name == "test"
        assert submission.data == {"field1": "test1"}
        assert response.status_code == 302
        assert response.url == "/thank-you/"
        submission_file = FormSubmissionFile.objects.get()
        assert submission_file.submission == submission
        assert submission_file.field_name == "field2"
        assert submission_file.file.read() == b"content"

    def test_base_form(self):
        form = MyForm({})
        assert form.is_valid()
        assert not form.saved
        form.cms_save(None, None)
        assert form.saved
