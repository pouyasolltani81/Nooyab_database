from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .services import GetUserToken

urlpatterns = [
    path('GetUserToken/', GetUserToken, name='get_user_token'),
] 

urlpatterns = format_suffix_patterns(urlpatterns)