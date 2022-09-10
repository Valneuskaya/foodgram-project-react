from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField
from django.db.models.functions import Length

CharField.register_lookup(Length)


class User(AbstractUser):
    email = EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True,
        help_text=('Must-fill form.'
                   'Max 254 letters.'
                   )
    )
    username = CharField(
        verbose_name='Unique username',
        max_length=150,
        unique=True,
        help_text=('Must-fill form.'
                   'From 1 to 150 letters.'),
    )
    first_name = CharField(
        verbose_name='First name',
        max_length=150,
        help_text=('Must-fill form.'
                   'From 1 to 150 letters.'),
    )
    last_name = CharField(
        verbose_name='Last name',
        max_length=150,
        help_text=('Must-fill form.'
                   'From 1 to 150 letters.'),
    )
    password = CharField(
        verbose_name='Password',
        max_length=150,
        help_text=('Must-fill form.'
                   'From 1 to 150 letters.'),
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('username',)

    def __str__(self):
        return f'{self.username}: {self.email}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Subscribed",
        related_name="subscribers",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Subscribed to",
        related_name="subscribed_authors",
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"{self.user}_to_{self.author}"
