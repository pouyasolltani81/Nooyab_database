from django.contrib import admin
from django.urls import path
from django.urls import include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [

    path('swagger-yaml/', SpectacularAPIView.as_view(), name='swagger-yaml'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='swagger-yaml'), name='swagger'),
    path("__reload__/", include("django_browser_reload.urls")),

    path('admin/', admin.site.urls),
    path('User/', include('UserModel.urls')),
    path('Auth/', include('AuthModel.urls')),
    path('Log/', include('LogModel.urls')),
    
    
    
    path('working-nobaan-data/', include('working_noban_data.urls')),
]