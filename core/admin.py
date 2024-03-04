from django.contrib import admin
from core.models import *
# Register your models here.

# admin.site.register(Customer)
admin.site.register(Category)
# admin.site.register(Product)
class proAdmin(admin.ModelAdmin):
    list_display = ('id','name','category','desc','price','product_available_cnt','img')
#
# #Register models on admin panel (class names)
admin.site.register(Product,proAdmin)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CheckoutAdd)
