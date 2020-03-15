from django import forms
from django.http import HttpResponse, HttpResponseRedirect

from cms_forms.forms import BaseForm
from cms_forms.importer import TypeReference
from cms_forms.plugin_forms.forms import FormForm

from .models import ContactSubmission


class ContactForm(BaseForm):
    name = forms.CharField()
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    def cms_save(self, request, plugin):
        ContactSubmission.objects.create(
            name=self.cleaned_data["name"], email=self.cleaned_data["email"], content=self.cleaned_data["content"],
        )
        return HttpResponseRedirect("/thank-you/")  # redirect on success
        return HttpResponse("<h1>Thank you!</h1>")  # display success message


class ContactFormForm(FormForm):
    form_type = TypeReference(ContactForm)
