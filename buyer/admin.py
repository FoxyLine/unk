from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Buyer,
    InternetAccount,
    Mobile,
    Stuff,
    MobileNumber,
    StuffType,
    InternetAccount,
    Clad,
)


class MobileInline(admin.TabularInline):
    model = Buyer.mobiles.through


class CladInline(admin.TabularInline):
    model = Buyer.clads.through


class InternetAccountInline(admin.TabularInline):
    model = Buyer.accounts.through
    extra = 1
    max_num = 1


class MobileNumbersInline(admin.TabularInline):
    model = Buyer.mobile_numbers.through


class StuffTInline(admin.TabularInline):
    model = Buyer.stuffs.through


class StuffAdmin(admin.ModelAdmin):
    pass


class CladAdmin(admin.ModelAdmin):
    pass


class StuffTypeAdmin(admin.ModelAdmin):
    pass


class MobileAdmin(admin.ModelAdmin):
    pass


class MobileNumberAdmin(admin.ModelAdmin):
    pass


class BuyerAdmin(admin.ModelAdmin):
    inlines = [
        MobileInline,
        MobileNumbersInline,
        StuffTInline,
        InternetAccountInline,
        CladInline,
    ]
    pass


class BuyerAccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(MobileNumber, MobileNumberAdmin)
admin.site.register(Mobile, MobileAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Stuff, StuffAdmin)
admin.site.register(StuffType, StuffTypeAdmin)
admin.site.register(InternetAccount, BuyerAccountAdmin)
admin.site.register(Clad, CladAdmin)
