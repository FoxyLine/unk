from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Buyer, BuyerAccount, Mobile, Stuff, MobileNumber, StuffType


class MobileInline(admin.TabularInline):
    model = Mobile


class MobileNumbersInline(admin.TabularInline):
    model = MobileNumber


class StuffTInline(admin.TabularInline):
    model = Stuff


class BuyerAccountInline(admin.TabularInline):
    model = BuyerAccount


class StuffAdmin(admin.ModelAdmin):
    pass


class StuffTypeAdmin(admin.ModelAdmin):
    pass


class MobileAdmin(admin.ModelAdmin):
    pass


class MobileNumberAdmin(admin.ModelAdmin):
    pass


class BuyerAdmin(admin.ModelAdmin):
    inlines = [MobileInline, MobileNumbersInline, StuffTInline, BuyerAccountInline]
    pass


class BuyerAccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(MobileNumber, MobileNumberAdmin)
admin.site.register(Mobile, MobileAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Stuff, StuffAdmin)
admin.site.register(StuffType, StuffTypeAdmin)
admin.site.register(BuyerAccount, BuyerAccountAdmin)
