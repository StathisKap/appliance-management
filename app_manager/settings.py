import json
import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-8wfqk2pk*)wg^k**)6(sywrg_q5kk1a2-lq57kdanmj^7%b=d6"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = json.loads(os.getenv("ALLOWED_HOSTS", "[]"))
print(ALLOWED_HOSTS)

# Application definition

INSTALLED_APPS = [
  "django.contrib.admin",
  "django.contrib.auth",
  "django.contrib.contenttypes",
  "django.contrib.sessions",
  "django.contrib.messages",
  "django.contrib.staticfiles",
  "appliance",
]

MIDDLEWARE = [
  "django.middleware.security.SecurityMiddleware",
  "whitenoise.middleware.WhiteNoiseMiddleware",
  "django.contrib.sessions.middleware.SessionMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.contrib.auth.middleware.AuthenticationMiddleware",
  "django.contrib.messages.middleware.MessageMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app_manager.urls"

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
      ],
    },
  },
]

WSGI_APPLICATION = "app_manager.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")

DATABASES = {
  "default": dj_database_url.config(
    env="DATABASE_URL", default=DATABASE_URL, conn_max_age=600
  )
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
  {
    "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
  },
  {
    "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
  },
  {
    "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
  },
  {
    "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
  },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging
##################################################
LOGGING = {
  "version": 1,
  "disable_existing_loggers": False,
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
    },
  },
  "root": {
    "handlers": ["console"],
    "level": "DEBUG" if DEBUG else "INFO",
  },
}


# Storage
##################################################

S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

STORAGES = {
  "default": {
    "BACKEND": "storages.backends.s3.S3Storage",
    "OPTIONS": {
      "access_key": S3_ACCESS_KEY,
      "secret_key": S3_SECRET_KEY,
      "bucket_name": S3_BUCKET_NAME,
      "endpoint_url": S3_ENDPOINT_URL,
      "addressing_style": "path",
    },
  },
  "staticfiles": {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
  },
}


# Security headers
##################################################

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# httpOnly for cookies
##################################################
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

AUTH_USER_MODEL = "appliance.User"


# Login URL
##################################################
LOGIN_URL = "/admin"
LOGIN_REDIRECT_URL = "/"