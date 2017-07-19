from django.contrib.auth import get_user_model


from esia_auth.gears import AbstractEsiaAuthBackend


class CustomEsiaAuthBackend(AbstractEsiaAuthBackend):
    def find_user(self, api, **kwargs):
        user = None
        create_user = kwargs.get('create_user', False)
        UserModel = get_user_model()

        if api:
            try:
                user = UserModel._default_manager.get(username=api.oid)
            except UserModel.DoesNotExist:
                if create_user:
                    user = UserModel._default_manager.create_user(username=api.oid)
        return user
