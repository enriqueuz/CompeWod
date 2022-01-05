""" Token authentication. """

# Django
from django.utils import timezone
from CompeWod.settings import TOKEN_EXPIRED_AFTER_SECONDS

# REST Framework
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

# Utils
from datetime import timedelta

class ExpiringTokenAuthentication(TokenAuthentication):
    """ Token authentication class with token expiration. """

    def expires_in(self, token):
        """ Returns time left for the token to expire. """
        time_elapsed = timezone.now() - token.created
        return timedelta(seconds=TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed

    def is_token_expired(self, token):
        """ Returns true if token has expired. """
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self, token):
        """ Return token and if it expired. When expired delete 
        and create another. """
        is_expired = self.is_token_expired(token)

        if is_expired:
            print("TOKEN EXPIRED")
            token.delete()
            token = Token.objects.create(user=token.user)
            # NOTE: Maybe delete all user sessions?

        return is_expired, token

    def authenticate_credentials(self, key):
        """ Authenticate credentials and raise error if token has expired. """
        try:
            token = self.get_model().objects.select_related('user').get(key=key)
             
        except self.get_model().DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        
        # Necessary?
        # if not token.user.is_active:
        #     raise AuthenticationFailed('User inactive or deleted.')

        is_expired, token = self.token_expire_handler(token)

        if is_expired:
            raise AuthenticationFailed('Token has expired')

        return (token.user, token)