from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(temp)
admin.site.register(order_item)
admin.site.register(bill_details)
admin.site.register(formatt)