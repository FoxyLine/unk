from django.db import models
from buyer.models import (
    Stuff,
    Mobile,
    MobileNumber,
    InternetAccount,
    Bank,
    Crypto,
    OnlinePay,
    Clad,
)


class PhotoMasterClad(models.Model):
    describe = models.CharField(max_length=255)
    image = models.ImageField()

    buyer = models.ForeignKey("Seller", on_delete=models.DO_NOTHING)


class PhotoClad(models.Model):
    describe = models.CharField(max_length=255)
    image = models.ImageField()

    buyer = models.ForeignKey("Seller", on_delete=models.DO_NOTHING)


class Curator(models.Model):
    curator_nickname = models.CharField(verbose_name="Ник куратора", max_length=255)
    curator_account = models.CharField(verbose_name="Аккаунт куратора", max_length=255)


class Seller(models.Model):
    stuffs = models.ManyToManyField(
        Stuff, through="SellerStuff", related_name="seller_stuffs"
    )
    mobiles = models.ManyToManyField(
        Mobile, default=None, through="SellerMobile", related_name="seller_mobiles"
    )
    mobile_numbers = models.ManyToManyField(
        MobileNumber,
        default=None,
        through="SellerMobileNumber",
        related_name="seller_mobile_numbers",
    )
    clads = models.ManyToManyField(Clad, through="SellerClads")
    master_clads = models.ManyToManyField(
        Clad, through="SellerMasterClads", related_name="seller_master_clads"
    )

    curators = models.ManyToManyField(Curator, through="SellerCurator")
    interner_accounts = models.ManyToManyField(
        InternetAccount, through="SellerInternerAccount"
    )
    banks = models.ManyToManyField(Bank, related_name="seller_buyers", blank=True)
    cryptos = models.ManyToManyField(Crypto, related_name="seller_buyers", blank=True)
    online_pays = models.ManyToManyField(
        OnlinePay, related_name="seller_buyers", blank=True
    )

    first_name = models.CharField(
        verbose_name="Имя", max_length=255, null=True, blank=True
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=255, null=True, blank=True
    )
    patronymic = models.CharField(
        verbose_name="Отчество", max_length=255, null=True, blank=True
    )

    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)

    password = models.CharField(
        verbose_name="Пароль", max_length=255, null=True, blank=True
    )

    shop_name = models.CharField(
        verbose_name="Название магазина", max_length=500, null=True, blank=True
    )
    shop_info = models.CharField(
        verbose_name="Информация о магазине", max_length=500, null=True, blank=True
    )

    account = models.CharField(
        verbose_name="Аккаунт", max_length=255, null=True, blank=True
    )

    SHOP_CHOICES = (
        ("Банковская карта", "Банковская карта"),
        ("Электронные платежи", "Электронные платежи"),
        ("Криптовалюта", "Криптовалюта"),
    )
    shop_type = models.CharField(
        max_length=500,
        verbose_name="Тип магазина",
        null=True,
        blank=True,
        choices=SHOP_CHOICES,
        default=None,
    )
    shop_address = models.CharField(
        max_length=500, null=True, blank=True, verbose_name="Адрес", default=None
    )
    shop_messanger_name = models.CharField(
        max_length=500,
        verbose_name="Наименование мессенджера",
        null=True,
        blank=True,
        default=None,
    )
    payment = models.CharField(
        max_length=255,
        verbose_name="Способ оплаты",
        null=True,
        blank=True,
        choices=SHOP_CHOICES,
    )

    CRIME_PLACE_CHOICES = [
        ("Кандалакшский района", "Кандалакшский района"),
        ("Ковдорский район", "Ковдорский район"),
        ("Кольский район", "Кольский район"),
        ("Ловозерский район", "Ловозерский район"),
        ("Печенгский район", "Печенгский район"),
        ("Терский район", "Терский район"),
        ("город Мурманск", "город Мурманск"),
        (
            "город Апатиты с подведомственной территорией",
            "город Апатиты с подведомственной территорией",
        ),
        (
            "ород Кировск с подведомственной территорией",
            "город Кировск с подведомственной территорией",
        ),
        (
            "город Оленегорск с подведомственной территорией",
            "город Оленегорск с подведомственной территорией",
        ),
        (
            "город Полярные Зори с подведомственной территорией",
            "город Полярные Зори с подведомственной территорией",
        ),
        ("ЗАТО посёлок Видяево", "ЗАТО посёлок Видяево"),
        ("ЗАТО город Заозёрск", "ЗАТО город Заозёрск"),
        ("ЗАТО город Островной", "ЗАТО город Островной"),
        ("ЗАТО город Североморск", "ЗАТО город Североморск"),
        ("ЗАТО Александровск", "ЗАТО Александровск"),
        (
            "город Мончегорск с подведомственной территорией",
            "город Мончегорск с подведомственной территорией",
        ),
    ]

    crime_place = models.CharField(
        max_length=255,
        verbose_name="Место совершения преступления",
        choices=CRIME_PLACE_CHOICES,
        null=True,
        blank=True,
    )
    arrest_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата арреста"
    )

    master_clad_coordinates = models.CharField(max_length=255, null=True, blank=True)
    clad_coordinates = models.CharField(max_length=255, null=True, blank=True)


class SellerClads(models.Model):
    buyer = models.ForeignKey(Seller, on_delete=models.CASCADE)
    clad = models.ForeignKey(Clad, on_delete=models.CASCADE)


class SellerMasterClads(models.Model):
    buyer = models.ForeignKey(Seller, on_delete=models.CASCADE)
    clad = models.ForeignKey(Clad, on_delete=models.CASCADE)


class SellerStuff(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    mobile = models.ForeignKey(Stuff, on_delete=models.CASCADE)


class SellerMobile(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE)


class SellerMobileNumber(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    mobile_number = models.ForeignKey(MobileNumber, on_delete=models.CASCADE)


class SellerCurator(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    curator = models.ForeignKey(Curator, on_delete=models.CASCADE)


class SellerInternerAccount(models.Model):
    internet_account = models.ForeignKey(InternetAccount, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
