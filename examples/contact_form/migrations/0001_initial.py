# Generated by Django 2.2.11 on 2020-03-15 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactSubmission",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=255)),
                ("content", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
