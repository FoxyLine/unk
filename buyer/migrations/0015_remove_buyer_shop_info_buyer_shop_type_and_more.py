# Generated by Django 4.1.2 on 2022-10-20 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("buyer", "0014_stufftype_remove_stuff_name_stuff_stuff_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="buyer",
            name="shop_info",
        ),
        migrations.AddField(
            model_name="buyer",
            name="shop_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Мессенджер", "Мессенджер"),
                    ("Web-сайт", "Web-сайт"),
                    ("DarkNet", "DarkNet"),
                ],
                max_length=500,
                null=True,
                verbose_name="Тип магазина",
            ),
        ),
        migrations.AlterField(
            model_name="stuff",
            name="stuff_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="buyer.stufftype",
                verbose_name="Вещество",
            ),
        ),
    ]