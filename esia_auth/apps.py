from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthConfig(AppConfig):
    name = 'esia_auth'
    verbose_name = _('Esia META')
