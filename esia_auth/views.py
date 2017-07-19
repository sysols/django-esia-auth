from django.shortcuts import render, redirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings
from django.http.response import HttpResponseForbidden

from .utils import get_esia_auth


def esia_login_view(request):
    is_logout = 'logout' in request.GET
    code = request.GET.get('code')
    state = request.GET.get('state')
    origin = request.GET.get('origin')

    if is_logout:
        logout(request)
        return redirect(origin or '/')

    if code and state:
        user = authenticate(code=code, state=state, create_user=True)
        if user is None:
            raise Http404('No such user registered')
        login(request, user)
        return redirect(
            getattr(settings, 'ESIA_REDIRECT_AFTER_LOGIN', '/')
        )

    return HttpResponseForbidden('Forbidden options...')


def esia_oauth_link_view(request):
    esia_auth = get_esia_auth()

    if not request.user or request.user.is_anonymous():
        esia_login_url = esia_auth.get_auth_url()
        return redirect(esia_login_url)
    else:
        return redirect(
            reverse('esia_auth:login') + '?origin={}&logout'.format(request.path)
        )
