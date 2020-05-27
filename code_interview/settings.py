import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'j%4s9n79np!^nrq3&h4=6a8r2c^ex9s)gg3s(zsx((o@qll2yj'
DEBUG = True
ALLOWED_HOSTS = []

# Celery config

CELERY_BROKER_URL = 'pyamqp://'
CELERY_RESULT_BACKEND = 'redis://'

CELERY_TASK_ROUTES = {
    # WARNING: room.tasks still need explicit queue name when chaining.
    # see rooms.signals.dispatch_run_task. Help?
    'rooms.tasks.*': {'queue': 'callbacks'},
    'tasks.sandbox.run_user_code': {'queue': 'sandbox'}
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'channels',
    'rooms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'code_interview.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'code_interview.wsgi.application'
ASGI_APPLICATION = "code_interview.routing.application"

##### Channels-specific settings

redis_url = 'redis://'

# Channel layer definitions
# http://channels.readthedocs.io/en/latest/topics/channel_layers.html
CHANNEL_LAYERS = {
    # "default": {
    #     # This example app uses the Redis channel layer implementation channels_redis
    #     "BACKEND": "channels_redis.core.RedisChannelLayer",
    #     "CONFIG": {
    #         "hosts": [redis_url,],
    #     },
    # },
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

CORS_ORIGIN_WHITELIST = [
    'http://localhost:8080' # front-end
]

# REST framework
default_renderers = []
if DEBUG:
    default_renderers = ['rest_framework.renderers.BrowsableAPIRenderer']

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ] + default_renderers,
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
