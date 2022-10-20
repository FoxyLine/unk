# Generated by Django 4.1.2 on 2022-10-15 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CrimePlace",
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
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
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
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Stuff",
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
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Seller",
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
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("patronymic", models.CharField(max_length=255)),
                ("birth_date", models.DateField()),
                ("imei", models.CharField(max_length=255)),
                ("mobile_brand", models.CharField(max_length=255)),
                ("mobile_model", models.CharField(max_length=255)),
                ("password", models.CharField(max_length=255)),
                ("mobile_number", models.CharField(max_length=255)),
                ("stuff_mass", models.DecimalField(decimal_places=4, max_digits=8)),
                ("unit", models.CharField(max_length=255)),
                ("shop_name", models.CharField(max_length=500)),
                ("shop_info", models.CharField(max_length=500)),
                ("account", models.CharField(max_length=255)),
                ("curator_nickname", models.CharField(max_length=255)),
                ("curator_account", models.CharField(max_length=255)),
                ("arrest_date", models.DateTimeField()),
                ("master_clad_coordinates", models.CharField(max_length=255)),
                ("clad_coordinates", models.CharField(max_length=255)),
                (
                    "crime_place",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="seller.crimeplace",
                    ),
                ),
                (
                    "payment_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="seller.payment",
                    ),
                ),
                (
                    "stuff_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="seller.stuff",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PhotoMasterClad",
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
                ("describe", models.CharField(max_length=255)),
                ("image", models.ImageField(upload_to="")),
                (
                    "buyer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="seller.seller",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PhotoClad",
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
                ("describe", models.CharField(max_length=255)),
                ("image", models.ImageField(upload_to="")),
                (
                    "buyer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="seller.seller",
                    ),
                ),
            ],
        ),
    ]