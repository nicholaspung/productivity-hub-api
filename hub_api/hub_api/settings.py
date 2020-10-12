import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG") == 'True'

ALLOWED_HOSTS = []
if os.getenv("ALLOWED_HOSTS_DOMAIN") and os.getenv("ALLOWED_HOSTS_IP_ADDRESS"):
    ALLOWED_HOSTS.append(os.getenv("ALLOWED_HOSTS_DOMAIN"))
    ALLOWED_HOSTS.append(os.getenv("ALLOWED_HOSTS_IP_ADDRESS"))

INSTALLED_APPS = [
    # Default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third Party
    'rest_framework',
    'corsheaders',
    'django_apscheduler',
    # Internal
    'firebase_auth.apps.FirebaseAuthConfig',
    'habit_tracker.apps.HabitTrackerConfig',
    'post_saver.apps.PostSaverConfig',
]

MIDDLEWARE = [
    # Third Party
    'corsheaders.middleware.CorsMiddleware',
    # Default
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hub_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hub_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'firebase_auth.authentication.FirebaseAuthentication',
    ),
}

CORS_ALLOWED_ORIGINS = []
if DEBUG:
    CORS_ALLOWED_ORIGINS.append("http://127.0.0.1:3000")
    CORS_ALLOWED_ORIGINS.append("http://localhost:3000")
elif os.getenv("CORS_ALLOWED_ORIGINS"):
    CORS_ALLOWED_ORIGINS.append(os.getenv("CORS_ALLOWED_ORIGINS"))

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
