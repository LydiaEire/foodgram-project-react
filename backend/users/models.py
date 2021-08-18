from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils import timezone


class FoodgramUserManager(BaseUserManager):
    # Создаём метод для создания пользователя
    def _create_user(self, email, username, password, **extra_fields):
        # Проверяем есть ли Email
        if not email:
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Email")
        # Проверяем есть ли логин
        if not username:
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Логин")
        # Делаем пользователя
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем всё остальное
        user.save(using=self._db)
        # Возвращаем пользователя
        return user

    # Делаем метод для создание обычного пользователя
    def create_user(self, email, username, password):
        # Возвращаем нового созданного пользователя
        return self._create_user(email, username, password)

    # Делаем метод для создание админа сайта
    def create_superuser(self, email, username, password):
        # Возвращаем нового созданного админа
        return self._create_user(email, username, password, is_staff=True, is_superuser=True)


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
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Email & Password are required by default.

    objects = FoodgramUserManager()

    class Meta:
        ordering = ('username',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def is_admin(self):
        return self.is_staff


class Follow(models.Model):
    """
    'Follow' model is described
    """

    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='User'
    )
    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='who is followed'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name='Time of creation'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_sub'
            )
        ]

    def __str__(self):
        return f'{self.user} following {self.author}'
