# Generated by Django 5.1.6 on 2025-03-09 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sde", "0014_alter_npccorporationdivision_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="npccorporation",
            name="shares",
            field=models.BigIntegerField(),
        ),
    ]
