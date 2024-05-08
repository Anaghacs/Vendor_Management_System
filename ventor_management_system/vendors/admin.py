from django.contrib import admin

from vendors.models import Vendor, PurchaseOrder
# Register your models here.

admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
