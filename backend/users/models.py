from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils import timezone


class FoodgramUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class FoodgramUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(max_length=150, verbose_name='Name')
    last_name = models.CharField(max_length=150, verbose_name='Surname')
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name='Registration date'
    )
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_superuser = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']  # Email & Password are required by default.

    objects = FoodgramUserManager()

    class Meta:
        ordering = ('username',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin
