from django.contrib import admin

from .models import *


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price','category']

admin.site.register(Customer)
admin.site.register(Product, AdminProduct)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(Material)
admin.site.register(Orderplaced)
# Register your models here.
admin.site.site_header = 'Kosh Furnitures'                    # default: "Django Administration"
admin.site.index_title = 'Admin panel'                 # default: "Site administration"
admin.site.site_title = 'HTML title from adminsitration' # default: "Django site admin"