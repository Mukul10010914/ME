from django.contrib import admin

# Register your models here.
from .models import recipient, transport
admin.site.register(transport)
admin.site.register(recipient)