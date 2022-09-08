from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, ManyToManyField
from django.db.models.functions import Length
from django.utils.translation import gettext_lazy as _

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
        verbose_name=_('Password'),
        max_length=150,
        help_text=('Must-fill form.'
                   'From 1 to 150 letters.'),
    )
    subscribe = ManyToManyField(
        verbose_name='Subscription',
        related_name='subscribers',
        to='self',
        symmetrical=False,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('username',)

    def __str__(self):
        return f'{self.username}: {self.email}'
