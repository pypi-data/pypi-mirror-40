from rest_framework.permissions import BasePermission
import base64
from django.conf import settings


class Paycom_Permissions(BasePermission):
    def has_permission(self, request, view):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split('Basic')
            decode_key = base64.b64decode(token[1])
            secret_key = str(decode_key, 'utf-8').split('Paycom:')
            if secret_key[1] == settings.PAYCOM_SETTINGS['SECRET_KEY']:
                return True
            else:
                return False
        except:
            return False