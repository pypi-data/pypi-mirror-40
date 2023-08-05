"""
Authentication classes for REST.
"""
from typing import Optional

from django.conf import settings
from rest_framework.request import Request
from rest_framework.authentication import TokenAuthentication


class BodyTokenAuthentication(TokenAuthentication) -> Optional[tuple]:
    '''Accept token in HTTP body. The field name is configurable, default is "access_token"'''
    def authenticate(self, request: Request):
        field_name = getattr(settings, 'REST_BODY_TOKEN_FIELD', 'access_token')
        key = request.data.get(field_name)
        if key:
            key = key.strip()
        # Skip if key is empty
        if not key:
            return None
        return self.authenticate_credentials(key)
