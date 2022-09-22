"""
Django settings for the TIaaS project.

Site-specifig options must be set in `config/local_settings.py`
(see `local_settings.py.template`). If you use a different location,
you need to edit the import statement at the end of this file.

For the full list of Django settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/

Production deployment checklist
https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
"""

import os
from tiaas import git

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_countries",
    "django.contrib.humanize",
    "bootstrap3",
    "training",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tiaas.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, 'templates'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "training.context_processors.settings",
            ]
        },
    }
]

WSGI_APPLICATION = "tiaas.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# --> Defined in config.local_settings


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/tiaas/static/"
STATIC_ROOT = "./static"

# Installation-specific settings

TIAAS_LOG_FILE = None         # Add path in local conf to enable
GALAXY_SECRET = "USING THE DEFAULT IS NOT SECURE!"
TIAAS_OWNER = "Galaxy Antartica" # A human-readable name
TIAAS_EMAIL = "admin@example.org"
TIAAS_OWNER_SITE = "https://example.org" # Your website, if you have one.
TIAAS_DOMAIN = "https://galaxy.example.org" # Your Galaxy instance

LOGOUT_REDIRECT_URL = '/tiaas/'

# Expose the username publicly in the status page, rather than an encoded ID.
TIAAS_EXPOSE_USERNAME = False

# Default period to retain contact information (months)
TIAAS_SHOW_ADVERTISING = True
TIAAS_GDPR_RETAIN_EXTRA_MONTHS = 12
TIAAS_LATE_REQUEST_PREVENTION_DAYS = 10   # calendar days

# EMAIL_HOST
# EMAIL_PORT
# EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD
# EMAIL_USE_TLS
# EMAIL_USE_SSL

# Default "from" address for automated email
TIAAS_SEND_EMAIL_TO = "admin@example.org" # Your admin email
TIAAS_SEND_EMAIL_FROM = None # "tiaas+noreply@example.org", setting to None leaves this feature disabled.
TIAAS_SEND_EMAIL_TO_REQUESTER = False # If you'd like to inform them of a successful request.


DOCUMENTATION = """
We want to help you conduct your training seminars. Where you provide the
training, we can provide you training infrastructure as a service (TIaaS). Some
of the benefits of using our infrastructure:

- Private queue, no wait times
- No Galaxy Maintenance
- No Galaxy Administration
- Free

Please note that we do provide this service for free to everyone, so we ask you
kindly likewise ensure that no one is restricted in their participation (e.g.
due to gender/age/race/too high course fees/etc.). You can read more [about TIaaS
on it's info page](https://galaxyproject.eu/tiaas)
"""


#############
# END TIAAS #
#############


try:
    from config.local_settings import *  # noqa: F401,F403  ignore these flake8 errors
except Exception as e:
    import sys
    sys.exit('Local settings file not found: %s' % e)

if TIAAS_LOG_FILE:
    from tiaas.logging import LOGGING
    LOGGING['handlers']['file']['filename'] = TIAAS_LOG_FILE

GIT_COMMIT_ID = git.get_commit_id(BASE_DIR)
GIT_REMOTE_URL = git.get_remote_url(BASE_DIR)
