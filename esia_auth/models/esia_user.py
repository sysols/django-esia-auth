from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class ESIACompatibleUserQuerySet(models.QuerySet):
    pass


class EsiaCompatibleUserManager(UserManager.from_queryset(ESIACompatibleUserQuerySet)):
    use_for_related_fields = True

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class ESIACompatibleUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()
    objects = EsiaCompatibleUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # логин или идентификатор пользователя
    username = models.CharField(
        _('Username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    # Может быть пустым, для пользователей авторизовавшихся через есиа.
    password = models.CharField(
        _('password'), max_length=128,
        blank=True, null=True
    )

    first_name = models.CharField(
        _('First name'), max_length=30,
        blank=True, null=True
    )
    last_name = models.CharField(
        _('Last name'), max_length=30,
        blank=True, null=True
    )
    email = models.EmailField(
        _('Email'),
        blank=True, null=True
    )
    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )
    last_login = models.DateTimeField(
        _('last login'),
        blank=True, null=True
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = True

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name or '', self.last_name or '')
        full_name = full_name.strip()
        if not full_name:
            full_name = self.username
        return full_name

    def get_short_name(self):
        first_name = self.first_name
        if not first_name:
            first_name = self.username
        first_name = first_name.strip()
        return first_name
