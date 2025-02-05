# Generated by Django 5.1.5 on 2025-02-05 21:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("agents", "0005_module"),
    ]

    operations = [
        migrations.CreateModel(
            name="CognitiveController",
            fields=[
                (
                    "module_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="agents.module",
                    ),
                ),
            ],
            bases=("agents.module",),
        ),
    ]
