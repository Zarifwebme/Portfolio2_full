from django.conf import settings
from django.utils import translation


class DefaultUzLanguageMiddleware:
    """Use Uzbek as the initial language when user has not chosen one yet."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang_cookie_name = settings.LANGUAGE_COOKIE_NAME
        has_cookie = bool(request.COOKIES.get(lang_cookie_name))
        has_session = hasattr(request, "session") and bool(request.session.get(translation.LANGUAGE_SESSION_KEY))

        if not has_cookie and not has_session:
            translation.activate("uz")
            request.LANGUAGE_CODE = "uz"

        response = self.get_response(request)

        if not has_cookie and not has_session:
            response.set_cookie(lang_cookie_name, "uz")

        return response
