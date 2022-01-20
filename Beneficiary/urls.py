from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Beneficiary.views import add, addrecipient, addtransport, view

urlpatterns = [
    path('Add/', add, name='add'),
    path('View/', view, name='view'),
    path('addrecipient/', addrecipient, name='addrecipient'),
    path('addtransport/', addtransport, name='addtransport'),
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)