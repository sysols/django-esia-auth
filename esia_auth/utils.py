# -*- coding: utf-8 -*-
import os

from django.conf import settings

from esia_connector.client import EsiaAuth, EsiaSettings


def get_os_file(name):
    certs_dir = getattr(settings, 'ESIA_CERTS_DIR', 'certs')
    if name:
        return os.path.join(settings.BASE_DIR, certs_dir, name)
    return None


def get_esia_auth():
    esia_settings_object = EsiaSettings(
        esia_client_id=settings.ESIA_SETTINGS.get('CLIENT_ID'),
        redirect_uri=settings.ESIA_SETTINGS.get('REDIRECT_URL'),
        certificate_file=get_os_file(settings.ESIA_SETTINGS.get('CERTIFICATE')),
        private_key_file=get_os_file(settings.ESIA_SETTINGS.get('PRIVATE_KEY')),
        esia_token_check_key=get_os_file(
            settings.ESIA_SETTINGS.get('TOKEN_CHECK_KEY', None)),
        esia_service_url=settings.ESIA_SETTINGS.get('SERVICE_URL'),
        esia_scope=settings.ESIA_SETTINGS.get('SCOPE'))

    return EsiaAuth(esia_settings_object)
