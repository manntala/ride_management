# Generated by Django 5.1.5 on 2025-01-25 17:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rides", "0003_alter_rideevent_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rideevent",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
