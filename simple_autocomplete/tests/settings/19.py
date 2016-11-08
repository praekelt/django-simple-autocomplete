import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

ROOT_URLCONF = 'simple_autocomplete.urls'

INSTALLED_APPS = (
    'simple_autocomplete',
    'simple_autocomplete.tests',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

SECRET_KEY = 'SECRET_KEY'

SIMPLE_AUTOCOMPLETE = {'auth.user': {'search_field': 'username'}}
