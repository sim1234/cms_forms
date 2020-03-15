from django.contrib import admin

from .models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created"]
    date_hierarchy = "created"
    readonly_fields = ["created"]
