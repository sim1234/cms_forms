from django.contrib import admin

from .models import Form, FormField, FormWidget


@admin.register(Form)
class FromAdmin(admin.ModelAdmin):
    pass


@admin.register(FormField)
class FormFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(FormWidget)
class FormWidgetAdmin(admin.ModelAdmin):
    pass
