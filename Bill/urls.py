from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Bill.views import create, removep, create_step2, viewbill, render_pdf, deletebill, updatebillno, extract_data, extract_bill_data

urlpatterns = [
    path('Create/Select_Product', create, name='create'),
    path('Create/Select_Beneficiary', create_step2, name='create_step2'),
    path('removep/', removep, name='removep'),
    path('View/', viewbill, name='viewbill'),
    path('Render_pdf/', render_pdf, name='render_pdf'),
    path('updatebillno/', updatebillno, name='updatebillno'),
    path('extract_data/', extract_data, name='extract_data'),
    path('extract_bill_data/', extract_bill_data, name='extract_bill_data'),
    path('deletebill/', deletebill, name='deletebill'),
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)