from django.db import models
from UserModel.models import User

CREDENTIAL_TYPES = (
        ('app', 'App Credential'), # users have access to their own ASP by app credential only one app token is enough
        ('admin', 'Admin Credential'),  # users have access to their own ASP by admin credential need admin permission user
        ('user', 'User Credential'), # users have access to their own ASP by user credential need user_token
        ('none', 'No Credentail')
    )

class Connect(models.Model):
    
    type = models.CharField(max_length=10, choices=CREDENTIAL_TYPES, default='app') # credential type
    desc = models.CharField(max_length=255, default='')
    token = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Connect'
        verbose_name_plural = 'Connects'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.type} - {self.token}"

    @classmethod
    def create_connect(cls, type, desc, token):
        con, created = cls.objects.get_or_create(type=type, token=token)
        con.desc = desc
        con.save()
        return con
    @classmethod
    def get_active_connects(cls):
        cons = cls.objects.filter(is_active=True)
        return cons