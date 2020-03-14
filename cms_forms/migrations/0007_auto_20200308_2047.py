# Generated by Django 2.2.10 on 2020-03-08 19:47

import cms_forms.fields
from django.db import migrations
import django.forms.fields
import django.forms.forms


class Migration(migrations.Migration):

    dependencies = [
        ("cms_forms", "0006_auto_20200308_0101"),
    ]

    operations = [
        migrations.AlterField(
            model_name="form",
            name="form_type",
            field=cms_forms.fields.TypeReferenceField(default=django.forms.forms.Form, max_length=255),
        ),
        migrations.AlterField(
            model_name="formfield", name="field_parameters", field=cms_forms.fields.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="formfield",
            name="field_type",
            field=cms_forms.fields.TypeReferenceField(default=django.forms.fields.Field, max_length=255),
        ),
        migrations.AlterField(
            model_name="formfield",
            name="widget_parameters",
            field=cms_forms.fields.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="formfield",
            name="widget_type",
            field=cms_forms.fields.TypeReferenceField(blank=True, default=None, max_length=255, null=True),
        ),
    ]