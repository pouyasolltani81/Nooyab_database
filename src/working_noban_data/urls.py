from django.urls import path
from . import services

urlpatterns = [
    path('general_doctors/', services.get_nobaan_data_doctors, name='nobaan_data_doctors'),
    path('general_secretaries/', services.get_nobaan_data_secretary, name='nobaan_data_secretary'),
    path('general_clinics/', services.get_nobaan_data_clinics, name='nobaan_data_clinics'),
    path('general_bookings/', services.get_nobaan_data_bookings, name='nobaan_data_bookings'),
    path('custom_bookings_esterdad/', services.get_nobaan_data_esterdad, name='get_nobaan_data_esterdad'),
    
    
    
    path('general_users/', services.get_nobaan_data_users, name='nobaan_data_users'),
    path('custom/', services.get_nobaan_data_custom, name='nobaan_data_custom'),
]
