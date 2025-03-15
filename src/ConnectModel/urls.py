from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .services import GetorCreateConnection, GetConnections, GetCredential

urlpatterns = [
    path('GetorCreateConnection/', GetorCreateConnection, name='get_or_create_connection'),
    path('GetConnections/', GetConnections, name='get_connections'),
    path('GetCredential/', GetCredential, name='get_credential'),
] 

urlpatterns = format_suffix_patterns(urlpatterns)