# Generated by Django 4.1.2 on 2022-10-19 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("buyer", "0009_remove_mobilenumber_mobile_mobilenumber_buyer_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mobile",
            name="mobile_number",
        ),
    ]
