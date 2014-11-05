from rest_framework.authentication import TokenAuthentication
from dms.models.token import Token


class TokenAuth(TokenAuthentication):
    model = Token