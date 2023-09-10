import re

from matches.utilities import AlterMatchLikes


class ResetMatchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)

        user = getattr(request.user, 'user', None)
        company = getattr(request.user, 'company', None)

        match_rules = [
            (r'^/auth/user/\d+/?$', 'PATCH'),
            (r'^/experience/?$', 'POST'),
            (r'^/skills/?$', 'POST'),
            (r'^/auth/company/\d+/?$', 'PATCH'),
            (r'^/company-roles/add_roles/?$', 'POST'),
        ]

        # Verifica si la ruta y el método coinciden con alguna de las reglas
        for pattern, http_method in match_rules:
            if re.match(pattern, request.path) and http_method == request.method:
                if user:
                    AlterMatchLikes.alter_user(user)
                elif company:
                    AlterMatchLikes.alter_company(company)
                break
        # Code to be executed for each request/response after
        # the view is called.

        return response
