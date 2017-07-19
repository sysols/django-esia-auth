# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend

from .utils import get_esia_auth


def esia_connector_complete(code, state):
    # TODO: починить валидацию токена (нужно прикрутить ключ сервера ЕСИА)
    esia_auth = get_esia_auth()
    return esia_auth.complete_authorization(
        code, state, validate_token=False
    )


class AbstractEsiaAuthBackend(ModelBackend):
    def authenticate(self, **kwargs):
        code = kwargs.get('code', None)
        state = kwargs.get('state', None)

        api = None
        if code and state:
            # complete authorization
            api = self._complete_oauth(code, state)
        return self.find_user(api, **kwargs)

    def _complete_oauth(self, code, state):
        api = esia_connector_complete(code, state)
        return api

    def find_user(self, api, **kwargs):
        raise NotImplementedError('find_user must be implement')
