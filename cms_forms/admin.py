from django.contrib import admin

from .models import Form, FormField


@admin.register(Form)
class FromAdmin(admin.ModelAdmin):
    pass


@admin.register(FormField)
class FormFieldAdmin(admin.ModelAdmin):
    pass
