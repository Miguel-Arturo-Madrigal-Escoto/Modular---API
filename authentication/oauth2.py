import os

import requests
from django.contrib.sessions.models import Session
from django.forms.models import model_to_dict
from rest_framework.request import Request


class OAuth2:
    def __init__(self, provider: str, request: Request) -> None:
        self.oauth = {
            'google': {
                'authenticate_uri': os.environ.get('SOCIAL_AUTH_GOOGLE_AUTHENTICATE_URI', ''),
                'db_field': os.environ.get('SOCIAL_AUTH_GOOGLE_STATE_DB_FIELD', '')
            },
            'linkedin': {
                'authenticate_uri': os.environ.get('SOCIAL_AUTH_LINKEDIN_AUTHENTICATE_URI', ''),
                'db_field': os.environ.get('SOCIAL_AUTH_LINKEDIN_STATE_DB_FIELD', '')
            }
        }
        self.oauth_url = self.oauth.get(provider, '')['authenticate_uri']
        self.db_field = self.oauth.get(provider, '')['db_field']
        self.request = request

    def authenticate(self):
        sessions = Session.objects.all()
        session_keys = {}

        for session in sessions:
            # match the session with the incoming state query param and the
            # session (cookie) decoded data from the database
            session_keys[
                session.get_decoded().get(self.db_field, '')
            ] = model_to_dict(session)['session_key']

        session_id = session_keys[self.request.query_params.get('state', '')]

        params = {
            'state': self.request.query_params.get('state', ''),
            'code': self.request.query_params.get('code', ''),
            'scope': self.request.query_params.get('scope', ''),
            'authuser': self.request.query_params.get('authuser', ''),
            'prompt': self.request.query_params.get('prompt', '')
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'sessionid={ session_id }'
        }
        api_response = requests.post(self.oauth_url, params=params, headers=headers)
        return api_response.json()
