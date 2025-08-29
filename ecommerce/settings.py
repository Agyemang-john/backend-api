
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

from corsheaders.defaults import default_headers
from datetime import timedelta
from urllib.parse import urlparse, parse_qsl


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-axuc^8+em$b+dauz(!3f*#21^gho#q$5t$na0rd$w*yexhj2t-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'corsheaders',
    'rest_framework',
    "djoser",
    'social_django',
    'core',
    'social_accounts',
    'rest_framework_simplejwt.token_blacklist',
    'userauths',
    'product',
    'vendor',
    'order',
    'address',
    'customer',
    'payments',
    'newsletter',
    'ckeditor',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'core.middleware.CurrencyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'
# ASGI_APPLICATION = 'ecommerce.asgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': tmpPostgres.path.replace('/', ''),
        'USER': tmpPostgres.username,
        'PASSWORD': tmpPostgres.password,
        'HOST': tmpPostgres.hostname,
        'PORT': 5432,
        'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


if DEBUG:
    MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CKEDITOR_UPLOAD_PATH = 'uploads/'


# DigitalOcean Spaces configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "negromart-space"
AWS_S3_REGION_NAME = "sfo3"
AWS_S3_ENDPOINT_URL = f"https://{AWS_S3_REGION_NAME}.digitaloceanspaces.com"

# # CDN domain for serving public files
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_REGION_NAME}.cdn.digitaloceanspaces.com"
AWS_LOCATION = 'media'

AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400'
}

STORAGES = {
    "default": {  # Media files → Spaces
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}


STORAGES["staticfiles"] = {
    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
}
# if DEBUG:  # Local development
#     STORAGES["staticfiles"] = {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#     }
# else:  # Production
#     STORAGES["staticfiles"] = {
#         "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#         "OPTIONS": {
#             "bucket_name": AWS_STORAGE_BUCKET_NAME,
#             "region_name": AWS_S3_REGION_NAME,
#             "endpoint_url": AWS_S3_ENDPOINT_URL,
#         },
#     }

AUTHENTICATION_BACKENDS = [
    'userauths.backends.EmailOrPhoneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'userauths.User'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'userauths.authentication.CustomJWTAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],

    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '4000/day',
    #     'user': '1000/day',
    # }
}


#Paystack configuration
PAYSTACK_SECRET_KEY = "sk_test_08697652e07898b20f337875bdd241b668a2abaa"
PAYSTACK_PUBLIC_KEY = "pk_test_1a9405c84346cd5f9b41a65524aa546d859be3d0"

# DJOSER CONFIGURATION
SITE_NAME = "Negromart"
DOMAIN = os.getenv('DOMAIN')
FRONTEND_LOGIN_URL = os.getenv("FRONTEND_LOGIN_URL")

# Emailing settings
SITE_URL = os.getenv('FRONTEND_BASE_URL')   # set correctly in each environment
DEFAULT_FROM_EMAIL = "Negromart <no-reply@negromart.com>"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'oseiagyemanjohn@gmail.com'
EMAIL_HOST_PASSWORD = 'jrsbfgzjqvtytcdc'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'auth/password-reset/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'auth/activation/{uid}/{token}',
    'USER_CREATE_PASSWORD_RETYPE': False,
    # 'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,
    # 'SERIALIZERS': {
    #     # 'activation': 'djoser.serializers.ActivationSerializer',
    #     'resend_activation': 'djoser.serializers.SendEmailResetSerializer',
    # },
}

# Redis URL (set in .env)
REDIS_URL = os.getenv("REDIS_URL", default="redis://127.0.0.1:6379/1")

# Caches (Redis as default backend)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "MAX_CONNECTIONS": 50,  # pool size
            "IGNORE_EXCEPTIONS": True,  # fail silently if Redis is down
        },
    }
}

# Sessions stored in Redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Redis as broker
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

#celery settings
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

#SIMPLE JWT CONFIGURATION
AUTH_COOKIE = 'access'
AUTH_ACCESS_MAX_AGE = timedelta(hours=1).total_seconds()
AUTH_REFRESH_MAX_AGE = timedelta(days=60).total_seconds()
AUTH_COOKIE_SECURE = os.getenv('AUTH_COOKIE_SECURE')
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAMESITE = 'None'

from datetime import timedelta

SIMPLE_JWT = {
    # Access Token Lifetime - 1 hour to balance security and UX
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    
    # Refresh Token Lifetime - 60 days, for long-term sessions
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
    
    # Enable token rotation for better security
    'ROTATE_REFRESH_TOKENS': True,
    
    # Blacklist old refresh tokens after they are rotated
    'BLACKLIST_AFTER_ROTATION': False,
    
    # Algorithm for signing the JWT
    'ALGORITHM': 'HS256',
    
    # HTTP Header for token authorization
    'AUTH_HEADER_TYPES': ('Bearer',),

    
    # Enabling sliding token lifetimes for smoother sessions
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=1),  # Sliding token lifetime 1 hour
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=60),  # Refresh token sliding window
    
    # Token user class (use custom user model if required)
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    
    # Enable JTI claim for each token (JWT ID)
    'JTI_CLAIM': 'jti',

    # Security leeway for potential timing discrepancies
    'LEEWAY': 30,  # Allow a 30-second leeway for clock discrepancies
}

CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ["https://api.negromart.com"]

CORS_ALLOWED_ORIGINS = [
    "https://negromart.com",
    "https://www.negromart.com",
    "http://localhost:3000",  # Next.js frontend URL
    "http://159.223.143.103",  # Next.js frontend URL
    "https://frontend-sigma-khaki-70.vercel.app",  # Next.js frontend URL
]
# CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS.copy()

CORS_ALLOW_HEADERS = list(default_headers) + [
    "x-guest-cart",
    "X-Currency",
    "X-Recently-Viewed",
    "x-ssr-refresh",
    'cache-control',
]


#EXCHANGE RATE API
EXCHANGE_RATE_API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
