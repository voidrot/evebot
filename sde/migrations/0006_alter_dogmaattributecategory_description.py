# Generated by Django 5.1.6 on 2025-03-09 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sde", "0005_alter_ancestry_short_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dogmaattributecategory",
            name="description",
            field=models.TextField(default=None, null=True),
        ),
    ]
