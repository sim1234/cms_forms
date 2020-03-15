import logging

from django import forms
from django.apps import apps
from django.utils.translation import gettext_lazy as _

from ..importer import TypeReference
from ..models import Form
from ..forms import SavingForm


class BaseFormForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ("name", "auto_render_fields", "load")

    form_type = None

    def update_instance(self):
        self.instance.form_type = self.form_type

    def clean(self):
        res = super().clean()
        try:
            self.update_instance()
            self.instance.build_form_cls()()
        except Exception as e:
            logging.exception("Form creation failed")
            raise forms.ValidationError(_("Form creation failed: %(error)s"), params={"error": e})
        return res


class FormForm(BaseFormForm):
    form_type = TypeReference(forms.Form)


class BaseModelFormForm(FormForm):
    meta_parameters = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_meta_kwargs()

    def load_meta_kwargs(self):
        kwargs = self.instance.meta_parameters
        for param in self.meta_parameters:
            field = self.fields[param]
            field.initial = kwargs.get(param, field.initial)

    def get_meta_kwargs(self):
        return {param: self.cleaned_data[param] for param in self.meta_parameters}

    def update_instance(self):
        self.instance.meta_parameters = self.get_meta_kwargs()
        return super().update_instance()


class ModelFormForm(BaseModelFormForm):
    form_type = TypeReference(forms.ModelForm)
    meta_parameters = ["fields", "exclude"]

    model = forms.TypedChoiceField(coerce=TypeReference)
    fields = forms.CharField(required=False, empty_value=None, initial="__all__")
    exclude = forms.CharField(required=False, empty_value=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["model"].choices = [(TypeReference(model), TypeReference(model).str) for model in apps.get_models()]

    def get_meta_kwargs(self):
        kwargs = super().get_meta_kwargs()
        kwargs["model"] = self.cleaned_data["model"].type
        return kwargs

    def load_meta_kwargs(self):
        self.fields["model"].initial = self.instance.meta_parameters.get("model", self.fields["model"].initial)
        return super().load_meta_kwargs()


class SavingFormForm(BaseModelFormForm):
    form_type = TypeReference(SavingForm)
    meta_parameters = ["success_url", "success_content"]

    success_url = forms.CharField(required=False)
    success_content = forms.CharField(required=False, widget=forms.Textarea)
