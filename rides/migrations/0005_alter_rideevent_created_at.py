# Generated by Django 5.1.5 on 2025-01-25 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rides", "0004_alter_rideevent_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rideevent",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
