# Generated by Django 5.1.5 on 2025-02-05 00:59

import django_jsonform.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("goal_generation", "0007_remove_goalgeneration_output"),
    ]

    operations = [
        migrations.AddField(
            model_name="goalgeneration",
            name="output",
            field=django_jsonform.models.fields.JSONField(blank=True, null=True),
        ),
    ]
