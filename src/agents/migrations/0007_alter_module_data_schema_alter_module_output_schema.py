# Generated by Django 5.1.5 on 2025-02-05 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("agents", "0006_module_data_module_data_schema_module_output_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="module",
            name="data_schema",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="module",
            name="output_schema",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
