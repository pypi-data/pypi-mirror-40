# drf-url-token-auth

Simple token based authentication using rest_framework.
Clients should authenticate by passing the token key in the "?token="
HTTP parameter. The token parametter can be configured.

## Quick start

1. Add "gitlab_webhook" to INSTALLED_APPS:

```
INSTALLED_APPS = {
    ...
    "drf_url_token_auth"
}
```

2. Modify rest framework settings:

```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'drf_url_token_auth.authentication.UrlTokenAuthentication',
    )
}
```

3. Optionally, configure url parameter name (default: token)

```
DRF_URL_TOKEN_AUTH = {
    'PARAM_NAME': 'token'
}
```

_Dev notes_:
build package: python setup.py sdist
install: pip install --user drf-url-token-auth/dist/drf-url-token-auth-01.tar.gz
