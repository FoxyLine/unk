from django.contrib import admin
from .models import Seller


# Register your models here.
class SellerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Seller, SellerAdmin)
