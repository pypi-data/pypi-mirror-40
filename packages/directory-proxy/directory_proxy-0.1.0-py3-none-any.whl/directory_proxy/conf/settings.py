import os
import environ

from directory_components.constants import IP_RETRIEVER_NAME_IPWARE


env = environ.Env()
env.read_env()

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'raven.contrib.django.raven_compat',
    'revproxy',
    'directory_proxy'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'directory_components.middleware.IPRestrictorMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = env.bool('CORS_ORIGIN_ALLOW_ALL', False)

FEATURE_URL_PREFIX_ENABLED = env.bool('FEATURE_URL_PREFIX_ENABLED', False)
URL_PREFIX_DOMAIN = env.str('URL_PREFIX_DOMAIN', '')
ROOT_URLCONF = 'directory_proxy.conf.urls'

WSGI_APPLICATION = 'directory_proxy.conf.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_TZ = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# Sentry
RAVEN_CONFIG = {
    'dsn': env.str('SENTRY_DSN', ''),
}


# Logging for development
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True,
            },
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }
else:
    # Sentry logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': (
                    'raven.contrib.django.raven_compat.handlers.SentryHandler'
                ),
                'tags': {'custom-tag': 'x'},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ip-restrictor
IP_RESTRICTOR_SKIP_CHECK_ENABLED = env.bool(
    'IP_RESTRICTOR_SKIP_CHECK_ENABLED', False
)
IP_RESTRICTOR_SKIP_CHECK_SENDER_ID = env.str(
    'IP_RESTRICTOR_SKIP_CHECK_SENDER_ID', 'directory'
)
IP_RESTRICTOR_SKIP_CHECK_SECRET = env.str(
    'IP_RESTRICTOR_SKIP_CHECK_SECRET', ''
)
IP_RESTRICTOR_REMOTE_IP_ADDRESS_RETRIEVER = env.str(
    'IP_RESTRICTOR_REMOTE_IP_ADDRESS_RETRIEVER',
    IP_RETRIEVER_NAME_IPWARE
)
RESTRICT_ADMIN = env.bool('IP_RESTRICTOR_RESTRICT_ADMIN', True)
ALLOWED_ADMIN_IPS = env.list('IP_RESTRICTOR_ALLOWED_ADMIN_IPS', default=[])
ALLOWED_ADMIN_IP_RANGES = env.list(
    'IP_RESTRICTOR_ALLOWED_ADMIN_IP_RANGES', default=[]
)
RESTRICTED_APP_NAMES = ['']

UPSTREAM_DOMAIN = env.str('UPSTREAM_DOMAIN')
UPSTREAM_SIGNATURE_SECRET = env.str('UPSTREAM_SIGNATURE_SECRET')
UPSTREAM_SIGNATURE_SENDER_ID = env.str(
    'UPSTREAM_SIGNATURE_SENDER_ID', 'directory'
)
