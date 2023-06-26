import os

import requests
from rest_framework.request import Request


class OAuth2:
    def __init__(self, provider: str, request: Request) -> None:
        self.oauth_urls = {
            'google': os.environ.get('SOCIAL_AUTH_GOOGLE_AUTHENTICATE_URI')
        }
        self.oauth_url = self.oauth_urls.get(provider, '')
        self.request = request

    def authenticate(self):
        session_id = self.request.COOKIES.get('sessionid')

        params = {
            'state': self.request.query_params.get('state', ''),
            'code': self.request.query_params.get('code', ''),
            'scope': self.request.query_params.get('scope', ''),
            'authuser': self.request.query_params.get('authuser', ''),
            'prompt': self.request.query_params.get('prompt', ''),
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'sessionid={ session_id }',
        }
        api_response = requests.post(self.oauth_url, params=params, headers=headers)

        return api_response.json()
