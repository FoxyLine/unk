from django.db import models


class Stuff(models.Model):
    name = models.CharField(max_length=255)


class Payment(models.Model):
    name = models.CharField(max_length=255)


class CrimePlace(models.Model):
    name = models.CharField(max_length=255)


class PhotoMasterClad(models.Model):
    describe = models.CharField(max_length=255)
    image = models.ImageField()

    buyer = models.ForeignKey("Seller", on_delete=models.DO_NOTHING)


class PhotoClad(models.Model):
    describe = models.CharField(max_length=255)
    image = models.ImageField()

    buyer = models.ForeignKey("Seller", on_delete=models.DO_NOTHING)


class Seller(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)

    birth_date = models.DateField()

    imei = models.CharField(max_length=255)

    mobile_brand = models.CharField(max_length=255)
    mobile_model = models.CharField(max_length=255)

    password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=255)

    stuff_type = models.ForeignKey(Stuff, on_delete=models.DO_NOTHING)
    stuff_mass = models.DecimalField(max_digits=8, decimal_places=4)
    unit = models.CharField(max_length=255)

    shop_name = models.CharField(max_length=500)
    shop_info = models.CharField(max_length=500)

    account = models.CharField(max_length=255)

    curator_nickname = models.CharField(max_length=255)
    curator_account = models.CharField(max_length=255)

    payment_type = models.ForeignKey(Payment, on_delete=models.DO_NOTHING)

    crime_place = models.ForeignKey(CrimePlace, on_delete=models.DO_NOTHING)

    arrest_date = models.DateTimeField()

    master_clad_coordinates = models.CharField(max_length=255)
    clad_coordinates = models.CharField(max_length=255)
