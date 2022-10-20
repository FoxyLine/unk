# Generated by Django 4.1.2 on 2022-10-18 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("buyer", "0004_alter_buyer_account_alter_buyer_arrest_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mobile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "imei",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="IMEI-номер"
                    ),
                ),
                (
                    "mobile_brand",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Марка"
                    ),
                ),
                (
                    "mobile_model",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Модель"
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Пароль"
                    ),
                ),
                (
                    "mobile_number",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Номер телефона",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="buyer",
            name="imei",
        ),
        migrations.RemoveField(
            model_name="buyer",
            name="mobile_brand",
        ),
        migrations.RemoveField(
            model_name="buyer",
            name="mobile_model",
        ),
        migrations.RemoveField(
            model_name="buyer",
            name="mobile_number",
        ),
        migrations.RemoveField(
            model_name="buyer",
            name="password",
        ),
        migrations.CreateModel(
            name="MobileNumber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.IntegerField(default=7)),
                ("number", models.CharField(max_length=15)),
                (
                    "mobile",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="numbers",
                        to="buyer.mobile",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="mobile",
            name="buyer",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="mobiles",
                to="buyer.buyer",
            ),
        ),
    ]