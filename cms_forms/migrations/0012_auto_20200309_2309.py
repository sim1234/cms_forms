# Generated by Django 2.2.10 on 2020-03-09 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms_forms", "0011_auto_20200309_2241"),
    ]

    operations = [
        migrations.RemoveField(model_name="form", name="lazy_loaded",),
        migrations.AddField(
            model_name="form",
            name="load",
            field=models.CharField(
                choices=[
                    ("static", "Render normally"),
                    ("lazy", "Render empty and load after the page is loaded"),
                    ("reload", "Render normally and reload after the page is loaded"),
                ],
                default="reload",
                max_length=255,
            ),
        ),
    ]
