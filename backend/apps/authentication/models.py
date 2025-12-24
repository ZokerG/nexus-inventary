from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with role-based access control
    """
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        EXTERNO = 'EXTERNO', 'Externo'
    
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.EXTERNO,
        verbose_name='Rol'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_externo(self):
        return self.role == self.Role.EXTERNO
