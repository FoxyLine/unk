from email.policy import default
from django.db import models

import buyer

# Create your models here.


class StuffType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип вещества"
        verbose_name_plural = "Тип вещества"


class Stuff(models.Model):
    M_GRAMM = "мг"
    GRAMM = "г"
    KILO = "кг"
    UNIT_CHOICES = (
        (M_GRAMM, "мг"),
        (GRAMM, "г"),
        (KILO, "кг"),
    )
    buyer = models.ForeignKey(
        "Buyer", default=None, on_delete=models.DO_NOTHING, related_name="stuffs"
    )

    stuff_type = models.ForeignKey(
        StuffType, on_delete=models.DO_NOTHING, verbose_name="Вещество"
    )
    mass = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        verbose_name="Масса",
        null=True,
        blank=True,
    )
    unit = models.CharField(
        max_length=255,
        verbose_name="Единица измерения",
        choices=UNIT_CHOICES,
        default=M_GRAMM,
    )

    class Meta:
        verbose_name = "Вещество"
        verbose_name_plural = "Вещества"

    def __str__(self):
        return f"{self.stuff_type} {self.mass or 0} {self.unit or ''}."


# class Payment(models.Model):
#     name = models.CharField(max_length=255)


class CrimePlace(models.Model):
    name = models.CharField(max_length=255)


class PhotoClad(models.Model):
    describe = models.CharField(max_length=255)
    image = models.ImageField()

    buyer = models.ForeignKey("Buyer", on_delete=models.DO_NOTHING)


class Mobile(models.Model):
    buyer = models.ForeignKey(
        "Buyer", default=None, on_delete=models.DO_NOTHING, related_name="mobiles"
    )
    imei = models.CharField(
        max_length=255, verbose_name="IMEI-номер", null=True, blank=True
    )
    mobile_brand = models.CharField(
        max_length=255, verbose_name="Марка", null=True, blank=True
    )
    mobile_model = models.CharField(
        max_length=255, verbose_name="Модель", null=True, blank=True
    )
    password = models.CharField(
        max_length=255, verbose_name="Пароль", null=True, blank=True
    )

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"


class MobileNumber(models.Model):
    buyer = models.ForeignKey(
        "Buyer", default=None, on_delete=models.DO_NOTHING, related_name="numbers"
    )
    code = models.IntegerField(default=7, verbose_name="Код страны")
    number = models.CharField(max_length=15, verbose_name="Номер телефона")

    class Meta:
        verbose_name = "Номер телефона"
        verbose_name_plural = "Телефонные номера"


class Buyer(models.Model):

    first_name = models.CharField(
        max_length=255, verbose_name="Имя", null=True, blank=True
    )
    last_name = models.CharField(
        max_length=255, verbose_name="Фамилия", null=True, blank=True
    )
    patronymic = models.CharField(
        max_length=255, verbose_name="Отчество", null=True, blank=True
    )
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)

    SHOP_CHOICES = (
        ("Мессенджер", "Мессенджер"),
        ("Web-сайт", "Web-сайт"),
        ("DarkNet", "DarkNet"),
    )
    shop_name = models.CharField(
        max_length=500,
        verbose_name="Наименование интернет-магазина",
        null=True,
        blank=True,
    )

    shop_type = models.CharField(
        max_length=500,
        verbose_name="Тип магазина",
        null=True,
        blank=True,
        choices=SHOP_CHOICES,
    )
    shop_address = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="Адрес",
    )
    shop_messanger_name = models.CharField(
        max_length=500, verbose_name="Наименование мессенджера", null=True, blank=True
    )

    account_name = models.CharField(
        max_length=255, verbose_name="Имя аккаунта", null=True, blank=True
    )
    account_address = models.CharField(
        max_length=255, verbose_name="Аккаунт-адрес", null=True, blank=True
    )
    account_number = models.CharField(
        max_length=255, verbose_name="Абонентский номер", null=True, blank=True
    )
    account_login = models.CharField(
        max_length=255, verbose_name="Логин", null=True, blank=True
    )
    account_password = models.CharField(
        max_length=255, verbose_name="Пароль", null=True, blank=True
    )
    account_password_app = models.CharField(
        max_length=255, verbose_name="Пароль приложения", null=True, blank=True
    )

    operator_nickname = models.CharField(
        max_length=255, verbose_name="Ник-нейм оператора", null=True, blank=True
    )
    operator_account = models.CharField(
        max_length=255, verbose_name="Аккаунт оператора", null=True, blank=True
    )

    SHOP_CHOICES = (
        ("Банковская карта", "Банковская карта"),
        ("Электронные платежи", "Электронные платежи"),
        ("Криптовалюта", "Криптовалюта"),
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
        ("город Апатиты с подведомственной территорией", "город Апатиты с подведомственной территорией"),
        ("ород Кировск с подведомственной территорией","город Кировск с подведомственной территорией"),
        ("город Оленегорск с подведомственной территорией", "город Оленегорск с подведомственной территорией"),
        ("город Полярные Зори с подведомственной территорией", "город Полярные Зори с подведомственной территорией"),
        ("ЗАТО посёлок Видяево", "ЗАТО посёлок Видяево"),
        ("ЗАТО город Заозёрск", "ЗАТО город Заозёрск"),
        ("ЗАТО город Островной", "ЗАТО город Островной"),
        ("ЗАТО город Североморск", "ЗАТО город Североморск"),
        ("ЗАТО Александровск", "ЗАТО Александровск"),
        ("город Мончегорск с подведомственной территорией", "город Мончегорск с подведомственной территорией")
    ]

    crime_place = models.CharField(
        max_length=255,
        verbose_name="Место совершения преступления",
        choices=CRIME_PLACE_CHOICES,
        null=True,
        blank=True,
    )

    arrest_date = models.DateTimeField(
        verbose_name="Дата задержания", null=True, blank=True
    )
    clad_coordinates = models.CharField(
        max_length=255, verbose_name="Координаты клада", null=True, blank=True
    )

    class Meta:
        verbose_name = "Скупщик"
        verbose_name_plural = "Скупщики"

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''} {self.patronymic or ''} Дата ареста:{self.arrest_date}."
