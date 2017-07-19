from django.db import models
from django.utils.translation import ugettext_lazy as _

from esia_auth.models import ESIACompatibleUser


class CustomUser(ESIACompatibleUser):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
