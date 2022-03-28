"""
Django settings for tiaas project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "2-5r))q-sv-f(l9hbb^nfoqjxj#&+du0xv+vxxz)!$&q(wcp=j"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "training.apps.TrainingConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_countries",
    "django.contrib.humanize",
    "bootstrap3",
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
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "tiaas.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
# "default": {
# "ENGINE": "django.db.backends.sqlite3",
# "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
# },
# "galaxy": {
# "ENGINE": "django.db.backends.postgresql_psycopg2",
# "NAME": "postgres",
# "USER": "postgres",
# "PASSWORD": "postgres",
# "HOST": "localhost",
# "PORT": "5432",
# },
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/tiaas/static/"
STATIC_ROOT = "./static"

GALAXY_SECRET = "USING THE DEFAULT IS NOT SECURE!"
TIAAS_OWNER = "UseGalaxy.eu"
TIAAS_EMAIL = "galaxy@informatik.uni-freiburg.de"
TIAAS_OWNER_SITE = "https://galaxyproject.eu"
TIAAS_DOMAIN = "https://usegalaxy.eu"

TIAAS_SEND_EMAIL_TO = "root@localhost"
TIAAS_SEND_EMAIL_FROM = "tiaas+noreply@example.org"

TIAAS_SHOW_ADVERTISING = True

# EMAIL_HOST
# EMAIL_PORT
# EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD
# EMAIL_USE_TLS
# EMAIL_USE_SSL

TIAAS_GDPR_RETAIN_EXTRA = 12  # months


try:
    from config.local_settings import *
except Exception as e:
    print(e)


git_head = os.path.join(BASE_DIR, ".git", "HEAD")
# https://stackoverflow.com/questions/14989858/get-the-current-git-hash-in-a-python-script#21901260
# Open .git\HEAD file:
with open(git_head, "r") as git_head_file:
    # Contains e.g. ref: ref/heads/master if on "master"
    git_head_data = str(git_head_file.read()).strip()

# Open the correct file in .git\ref\heads\[branch]
git_head_ref = os.path.join(BASE_DIR, ".git", git_head_data.split(" ")[1])
# Get the commit hash ([:7] used to get "--short")

with open(git_head_ref, "r") as git_head_ref_file:
    GIT_COMMIT_ID = git_head_ref_file.read().strip()
