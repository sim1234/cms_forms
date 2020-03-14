from django import forms
from .models import FormSubmission


class BaseForm(forms.Form):
    """Interface for custom forms"""

    def cms_save(self, request, plugin):
        return getattr(self, "safe", lambda: None)()


class SavingForm(BaseForm):
    def cms_save(self, request, plugin):
        FormSubmission.objects.create(
            form_name=plugin.name, data=self.cleaned_data,
        )
