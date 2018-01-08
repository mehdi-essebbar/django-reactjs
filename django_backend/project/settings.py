"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

"""
TODO
-Change the database to MongoDB
-Connect to the remote Database
-Install mongoengine for DRF
-EDIT the models to adapt to the new environment
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import mongoengine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$!r)@8^pv#=wd7ksxso22sc#+=jc*e2ssyqihnh64+*lor_+-d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'rest_framework_mongoengine',
    
    'django_mongoengine',
    'django_mongoengine.mongo_auth',
    'django_mongoengine.mongo_admin',
    #'rest_framework.authtoken',
    #'rest_auth',
    #'rest_auth.registration',

    #'allauth',
    #'allauth.account',
    #'allauth.socialaccount',

    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.twitter',

    # rest cors support
    'corsheaders',

    #'django_backend.user_profile',
    #'django_backend.shops',
    'django_backend.restauth'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'django_backend/templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MONGODB_DATABASES = {
    "default": {
        "name": "project",
        "host": "mongodb://admin:azerty@cluster0-shard-00-00-uaelv.mongodb.net:27017,cluster0-shard-00-01-uaelv.mongodb.net:27017,cluster0-shard-00-02-uaelv.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin",
        "port": 27017,
        "tz_aware": True,  # if you use timezones in django (USE_TZ = True)
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SITE_ID = 1

# This is a dummy django model. It's just a crutch to keep django content,
# while all the real functionality is associated with MONGOENGINE_USER_DOCUMENT
AUTH_USER_MODEL = 'mongo_auth.MongoUser'

SESSION_ENGINE = 'django_mongoengine.sessions'

MONGOENGINE_USER_DOCUMENT = 'django_backend.restauth.models.User'

## User Authentication Settings

ACCOUNT_ADAPTER = 'django_backend.user_profile.adapter.MyAccountAdapter'
# Following is added to enable registration with email instead of username
AUTHENTICATION_BACKENDS = (
 # Needed to login by username in Django admin, regardless of `allauth`
 #"django.contrib.auth.backends.ModelBackend",
    'django_mongoengine.mongo_auth.backends.MongoEngineBackend',

 # `allauth` specific authentication methods, such as login by e-mail
 #"allauth.account.auth_backends.AuthenticationBackend",
)

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'django_backend.user_profile.serializers.UserSerializer'
}

REST_SESSION_LOGIN = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_USERNAME_REQUIRED = True
LOGOUT_ON_PASSWORD_CHANGE = False



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Change CORS settings as needed

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (

)

CORS_ORIGIN_REGEX_WHITELIST = (
    r'^(https?://)?localhost',
    r'^(https?://)?127.',
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'django_backend/tmp/emails'
DEFAULT_FROM_EMAIL = 'admin@admin.com'
ADMIN_EMAIL = 'admin@mail.com'
