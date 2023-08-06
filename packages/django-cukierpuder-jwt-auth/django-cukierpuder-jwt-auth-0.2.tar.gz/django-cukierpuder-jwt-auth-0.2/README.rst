=====
django-cukierpuder-jwt-auth
=====

django-cukierpuder-jwt-auth is a simple authorization Django app based on JSON Web Tokens.

Quick start
-----------

1. Add jwt_auth to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        'jwt_auth.apps.JwtAuthConfig',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('auth/', include('jwt_auth.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Available endpoints::

    '/auth/register/' - [POST] register a new user (requires an email, username and password in request's body)
    '/auth/token/obtain/' - [POST] obtain access and refresh token (requires username and password in request's body)
    '/auth/token/refresh' - [POST] obtain refresh token (requires refresh token in request's body)
    '/auth/users/' - [GET] get the list of all users (requires access token in request's header)
    '/auth/users/<int:id>/' - [GET] get the details of specific user (requires access token in request's header)