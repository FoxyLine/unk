# Generated by Django 4.1.2 on 2022-12-07 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buyer", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stufftype",
            name="name",
        ),
        migrations.AlterField(
            model_name="stufftype",
            name="id",
            field=models.CharField(
                max_length=255, primary_key=True, serialize=False, unique=True
            ),
        ),
    ]