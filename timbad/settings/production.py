import os
from django.conf import settings
import base

DATABASES = settings.DATABASES

DEBUG = False
TEMPLATE_DEBUG = False

#PRODUCTION SPECFIC APPS
base.INSTALLED_APPS += [
    'whitenoise',
]

#STATIC FILE MANAGEMENT
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(base.BASE_DIR,'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(base.BASE_DIR, 'static'),
)

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {
    "default": dj_database_url.config(default='postgres://localhost'),
}
DATABASES['default']['CONN_MAX_AGE'] = 500

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Allow all host headers
ALLOWED_HOSTS = ['*']

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}

#TEMPLATE MANAGEMENT
TEMPLATE_DIRS=(
    os.path.join(base.BASE_DIR, 'templates'),
    )