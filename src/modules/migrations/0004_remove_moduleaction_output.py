# Generated by Django 5.1.5 on 2025-02-12 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("modules", "0003_moduleaction_input_moduleaction_output_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="moduleaction",
            name="output",
        ),
    ]
