from functools import wraps

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseBadRequest, HttpResponseForbidden


try:
    COMMANDER_KEY = settings.COMMANDER_KEY
except AttributeError as exc:
    COMMANDER_KEY = None

# don't allow the default key in production
if COMMANDER_KEY == 's00pers3cret!' and not settings.DEBUG:
    raise ImproperlyConfigured('You can\'t use the example COMMANDER_KEY; change it to something else')


def protect_with_key(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if COMMANDER_KEY is None:
            return HttpResponseForbidden('Commander is disabled')
        if 'key' not in request.GET:
            return HttpResponseBadRequest('Make sure to include the ?key in your querystring')
        if request.GET['key'] != COMMANDER_KEY:
            return HttpResponseForbidden('Incorrect key')
        return view(request, *args, **kwargs)
    return wrapper
