from django.contrib import admin
from .models import Connect

class ConnectAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'desc', 'token', 'is_active', 'created_at', 'updated_at')
    search_fields = ('id', 'type')
    ordering = ('-created_at',)

admin.site.register(Connect, ConnectAdmin)