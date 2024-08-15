from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime



#Excepcion for user.password, rule=> 8<=password>=64
def validate_user_password(value):
    if len(value)>= 8 and len(value)<=64:
        return value
    else:
        raise ValidationError("Password entre 8 y 64 Caracteres")
    
class CustomUserManager(BaseUserManager):
    """ User manager"""
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        """
        Save an user using email, password and other fields
        """
        if not email:
            raise ValueError('Es necesario email valido')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        usuario = extra_fields.get('name')
        now = datetime.now()
        user_temp= usuario+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
        print(user_temp)

        extra_fields.setdefault('user',user_temp)

        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
        


class User(AbstractBaseUser, PermissionsMixin):
    """ User model"""
    email = models.EmailField(_('email'), unique=True, validators=[validate_email])
    name = models.CharField(_('name'), max_length=50, blank=False)
    last_name = models.CharField(_('last_name'), max_length=80, blank=False)
    password = models.CharField(_('password'), max_length=64, validators=[validate_user_password])
    phone = PhoneNumberField(unique=True)
    user = models.CharField(max_length=100, unique=True)

    is_superadmin = models.BooleanField(_('is_superadmin'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    """
    def save(self, *args, **kwargs):
        now = datetime.now()
        self.user= self.name+now.year+now.month+now.day+now.hour+now.minute+now.second
        print(self.user)
        super().save(*args, **kwargs)
    """

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """stirng representation"""
        return self.email