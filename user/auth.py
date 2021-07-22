from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

import jwt

from user.serializers import UserListSerializer
from user.models import UserModel

KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'

class JWTAuththentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = str(request.META.get('HTTP_AUTHORIZATION'))[7:]

            if not token:
                return None
            
            payload = jwt.decode(token, key=KEY, algorithms=ALGORITHM)
            user = UserModel.objects.get(id=payload['id'])
            if not user.exist:
                raise exceptions.AuthenticationFailed("Invalid token payload")
            serialized = UserListSerializer(data=user, many=False)
            return (serialized.data, None)
        except:
            raise exceptions.AuthenticationFailed('Token invalid')
