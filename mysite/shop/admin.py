from django.contrib import admin

# Register your models here.
from .models import myProduct, Contact, Orders, OrderUpdate

admin.site.register(myProduct)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)