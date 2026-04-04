from django.conf import settings
from django.shortcuts import render
from django.utils import translation


class DefaultUzLanguageMiddleware:
    """Use Uzbek as the initial language when user has not chosen one yet."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang_cookie_name = settings.LANGUAGE_COOKIE_NAME
        has_cookie = bool(request.COOKIES.get(lang_cookie_name))
        session_language = None
        if hasattr(request, "session"):
            session_language = request.session.get("django_language") or request.session.get("_language")
        has_session = bool(session_language)

        if not has_cookie and not has_session:
            translation.activate("uz")
            request.LANGUAGE_CODE = "uz"

        response = self.get_response(request)

        if not has_cookie and not has_session:
            response.set_cookie(lang_cookie_name, "uz")

        return response


class ErrorPageMiddleware:
    """Render a single custom error page for HTTP errors in production."""

    ERROR_STATUS_CODES = {400, 403, 404, 405, 500}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception:
            if settings.DEBUG:
                raise
            return render(request, "404.html", status=500)

        if settings.DEBUG:
            return response

        if response.status_code in self.ERROR_STATUS_CODES or response.status_code >= 500:
            return render(request, "404.html", status=response.status_code)

        return response
