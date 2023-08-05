from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


def get_authorization_param(request):
    param_name = 'token'
    if getattr(settings, 'DRF_URL_TOKEN_AUTH', False):
        url_token_auth = getattr(settings, 'DRF_URL_TOKEN_AUTH')
        param_name = url_token_auth.get('PARAM_NAME', param_name)
    return request.query_params.get(param_name)


class UrlTokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication using rest_framework.
    Clients should authenticate by passing the token key in the "?token="
    HTTP parameter.
    """

    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    def authenticate(self, request):
        # import pdb; pdb.set_trace();
        token = get_authorization_param(request)

        if not token:
            msg = _('Invalid token. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token. ' + key))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.'))

        return (token.user, token)
