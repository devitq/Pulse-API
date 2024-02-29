import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import Profile


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization", "").split("Bearer ")[-1]

        if not token:
            return None

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )

            user = Profile.objects.get(login=payload["login"])
        except Profile.DoesNotExist:
            error = "Invalid token"
            raise AuthenticationFailed(error) from None
        except jwt.ExpiredSignatureError:
            error = "Token has expired"
            raise AuthenticationFailed(error) from None
        except jwt.InvalidTokenError:
            error = "Invalid token"
            raise AuthenticationFailed(error) from None
        else:
            return (user, None)
