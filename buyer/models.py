from email.policy import default
from django.db import models
from django.core.validators import RegexValidator

import buyer

# Create your models here.


class StuffType(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)

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

    def std_mass(self):
        return Stuff.normalize_mass(self.mass, self.unit)

    @staticmethod
    def normalize_mass(mass, unit):
        return mass * {Stuff.GRAMM: 1000, Stuff.KILO: 1000 * 1000}.get(unit, 1)

    def __str__(self):
        return f"{self.stuff_type} {self.mass or 0} {self.unit or ''}."


class PhotoClad(models.Model):
    describe = models.CharField(max_length=255)
    image = models.ImageField(upload_to="files/", null=True, blank=True)

    buyer = models.ForeignKey("Buyer", on_delete=models.DO_NOTHING)


class Mobile(models.Model):
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
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Формат номера телефона должен соответствовать: '+XXXXXXXXX'. Максимальная длина - 15 цифр.",
    )

    number = models.CharField(
        # validators=[phone_regex],
        max_length=17,
        # unique=True,
        verbose_name="Номер телефона",
    )

    class Meta:
        verbose_name = "Номер телефона"
        verbose_name_plural = "Телефонные номера"


class InternetAccount(models.Model):
    login = models.CharField(
        verbose_name="Логин", max_length=100, null=True, blank=True
    )
    password = models.CharField(
        verbose_name="Пароль", max_length=100, null=True, blank=True
    )
    app_password = models.CharField(
        verbose_name="Пароль приложения", max_length=100, null=True, blank=True
    )
    name = models.CharField(
        verbose_name="Имя аккаунта", max_length=100, null=True, blank=True
    )
    account_address = models.CharField(
        verbose_name="«Аккаунт-адрес»", max_length=100, null=True, blank=True
    )
    number = models.CharField(
        verbose_name="Абонентский номер (привязанный к аккаунту)",
        max_length=100,
        null=True,
        blank=True,
    )

    operator_nickname = models.CharField(
        max_length=255, verbose_name="Ник-нейм оператора", null=True, blank=True
    )
    operator_account = models.CharField(
        max_length=255, verbose_name="Аккаунт оператора", null=True, blank=True
    )

    def __str__(self) -> str:
        return f"pk {self.pk} Логин: {self.login}, Пароль: {self.password}, Пароль приложения: {self.app_password}, Имя аккаунта: {self.name}, «Аккаунт-адрес»: {self.account_address}, Абонентский номер (привязанный к аккаунту): {self.number}, Ник-нейм оператора: {self.operator_nickname}, Аккаунт оператора: {self.operator_account}"

    class Meta:
        verbose_name = "Аккаунт пакупателя"
        verbose_name_plural = "Аккаунт пакупателя"


class Bank(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Название банка", null=True, blank=True
    )
    card_number = models.CharField(
        max_length=255, verbose_name="Номер банковской карты", null=True, blank=True
    )

    def __str__(self):
        return self.name or ""

    class Meta:
        verbose_name = "Банковские реквизиты"
        verbose_name_plural = "Банковские реквизиты"


class OnlinePay(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Название платежной системы", null=True, blank=True
    )
    account = models.CharField(
        max_length=255, verbose_name="Номер счета", null=True, blank=True
    )

    def __str__(self):
        return self.name or ""

    class Meta:
        verbose_name = "Онлайн-платежи"
        verbose_name_plural = "Онлайн-платежи"


class Crypto(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Название криптовалюты", null=True, blank=True
    )
    address_wallet = models.CharField(
        max_length=255, verbose_name="Адрес кошелька", null=True, blank=True
    )

    def __str__(self):
        return self.name or ""

    class Meta:
        verbose_name = "Криптовалюты"
        verbose_name_plural = "Криптовалюты"


class Buyer(models.Model):
    mobiles = models.ManyToManyField("Mobile", default=None, through="BuyerMobile")
    stuffs = models.ManyToManyField("Stuff", through="BuyerStuff")
    clads = models.ManyToManyField("Clad", through="BuyerClads")
    mobile_numbers = models.ManyToManyField(
        "MobileNumber", through="BuyerMobileNumber", related_name="buyer_mobile_numbers"
    )
    banks = models.ManyToManyField(Bank, related_name="buyers", blank=True)
    cryptos = models.ManyToManyField(Crypto, related_name="buyers", blank=True)
    online_pays = models.ManyToManyField(OnlinePay, related_name="buyers", blank=True)

    accounts = models.ManyToManyField(
        "InternetAccount",
        default=None,
        related_name="accounts",
    )

    first_name = models.CharField(
        max_length=255, verbose_name="Имя", null=True, blank=True, default=""
    )
    last_name = models.CharField(
        max_length=255, verbose_name="Фамилия", null=True, blank=True, default=""
    )
    patronymic = models.CharField(
        max_length=255, verbose_name="Отчество", null=True, blank=True, default=""
    )
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)

    MESSENGER = "Мессенджер"
    WEB_SITE = "Web-сайт"
    DARK_NET = "DarkNet"
    SHOP_CHOICES = (
        (MESSENGER, "Мессенджер"),
        (WEB_SITE, "Web-сайт"),
        (DARK_NET, "DarkNet"),
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

    PAYMENT_CHOICES = (
        ("Банковская карта", "Банковская карта"),
        ("Электронные платежи", "Электронные платежи"),
        ("Криптовалюта", "Криптовалюта"),
    )
    payment = models.CharField(
        max_length=255,
        verbose_name="Способ оплаты",
        null=True,
        blank=True,
        choices=PAYMENT_CHOICES,
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
        verbose_name="Дата задержания", null=True, blank=True
    )

    class Meta:
        verbose_name = "Скупщик"
        verbose_name_plural = "Скупщики"

    def get_account(self) -> InternetAccount:
        accounts = self.accounts.all()
        if len(accounts) > 1:
            raise "accounts > 1"
        return accounts[0] if accounts else None

    # def __str__(self):
    #     return f"{self.first_name or ''} {self.last_name or ''} {self.patronymic or ''} Дата ареста:{self.arrest_date}. Вещества: {','.join([s.stuff_type.name for s in self.stuffs.all()])}"


class Clad(models.Model):
    MASTER_CLAD = "Мастер-клад"
    CLAD = "Закладка"
    TYPE_CLAD_CHOICES = (
        (MASTER_CLAD, "Мастер-клад"),
        (CLAD, "Закладка"),
    )
    type_clad = models.CharField(
        max_length=25, choices=TYPE_CLAD_CHOICES, blank=True, null=True, default=CLAD
    )
    lng = models.DecimalField(
        max_digits=11,
        decimal_places=8,
        verbose_name="Координаты клада (долгота)",
        null=True,
        blank=True,
    )
    lat = models.DecimalField(
        max_digits=11,
        decimal_places=8,
        verbose_name="Координаты клада (Ширина)",
        null=True,
        blank=True,
    )
    photo = models.ImageField(
        verbose_name="Фотография клада",
        null=True,
        blank=True,
    )


class BuyerClads(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    clad = models.ForeignKey(Clad, on_delete=models.CASCADE)


class BuyerMobile(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE)


class BuyerStuff(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    mobile = models.ForeignKey(Stuff, on_delete=models.CASCADE)


class BuyerMobileNumber(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    mobile_number = models.ForeignKey(MobileNumber, on_delete=models.CASCADE)
