# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from .utils import get_esia_auth


def esia_connector_complete(code, state):
    # TODO: починить валидацию токена (нужно прикрутить ключ сервера ЕСИА)
    esia_auth = get_esia_auth()
    return esia_auth.complete_authorization(
        code, state, validate_token=False
    )


class EsiaAuthBackend(ModelBackend):
    def authenticate(self, **kwargs):
        code = kwargs.get('code', None)
        state = kwargs.get('state', None)

        api = None
        if code and state:
            # complete authorization
            api = self._complete_oauth(code, state)

        user = self.find_user(api, **kwargs)
        if user and api:
            self.update_user(user, api)
        return user

    @staticmethod
    def _complete_oauth(code, state):
        api = esia_connector_complete(code, state)
        return api

    def find_user(self, api, **kwargs):
        user = None
        create_user = kwargs.get('create_user', False)
        UserModel = get_user_model()

        if api:
            try:
                user = UserModel.objects.get(username=api.oid)
            except UserModel.DoesNotExist:
                if create_user:
                    user = UserModel.objects.create_user(username=api.oid)
        return user

    def update_user(self, user, api):
        self.update_info(user, api)
        self.update_contacts(user, api)
        user.save()

    @staticmethod
    def update_info(user, api):
        inf = api.get_person_main_info()
        user.last_name = inf.get('lastName')
        user.first_name = inf.get('firstName')

    @staticmethod
    def update_contacts(user, api):
        contacts = api.get_person_contacts()
        for c in contacts['elements']:
            if c['type'] == 'EML':
                user.email = c['value']
                break
