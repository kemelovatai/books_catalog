from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=100, verbose_name=_('Адрес эл. почты'))
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Фамилия'))

    is_active = models.BooleanField(default=True, verbose_name=_('Активный'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Статус персонала'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('Статус суперпользователя'))
    birthday = models.DateField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def has_usable_password(self):
        return super().has_usable_password() and self.password != ''

    def str(self):
        return self.email

    def change_password(self, password):
        self.set_password(password)
        self.save()
