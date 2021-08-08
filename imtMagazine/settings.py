import os
import json
from django.utils import timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

secret_file = os.path.join(BASE_DIR, 'secrets/secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

ENVIRONMENT = get_secret("ENVIRONMENT")
SECRET_KEY = get_secret("SECRET_KEY")
DEBUG = get_secret("DEBUG")

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0',]

X_FRAME_OPTIONS = 'SAMEORIGIN'

XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'magazine',
    'bootstrap4',
    'django_summernote',
    'crispy_forms',
    'six',
    'storages',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

SUMMERNOTE_CONFIG = {
    'attachment_filesize_limit': 5 * 1024 * 1024,  # specify the file size
    'width': '100%',
    'toolbar': [
        ['style', ['style']],
        ['font', ['bold', 'underline', 'clear']],
        ['fontname', ['fontname']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['table', ['table']],
        ['insert', ['link', 'picture', 'video']],
        ['view', ['fullscreen', 'codeview', 'help']],
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'imtMagazine.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'magazine/templates ')],
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

WSGI_APPLICATION = 'imtMagazine.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
if ENVIRONMENT == 'test':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = 'media/'

elif ENVIRONMENT == 'dev':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = 'media/'

elif ENVIRONMENT == 'real':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': get_secret("DATABASE")['DB_NAME'],
            'USER': get_secret("DATABASE")['DB_USER'],
            'PASSWORD': get_secret("DATABASE")['DB_PW'],
            'HOST': get_secret("DATABASE")['DB_HOST'],
            'PORT': get_secret("DATABASE")['DB_PORT']
        }
    }

    AWS_ACCESS_KEY_ID = get_secret("AWS_S3")['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = get_secret("AWS_S3")['AWS_SECRET_ACCESS_KEY']
    AWS_S3_REGION_NAME = get_secret("AWS_S3")['AWS_S3_REGION_NAME']
    AWS_STORAGE_BUCKET_NAME = get_secret("AWS_S3")['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
    AWS_DEFAULT_ACL = 'public-read'

    STATIC_URL = '/static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    STATICFILES_STORAGE = 'magazine.storage.S3StaticStorage'

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    DEFAULT_FILE_STORAGE = 'magazine.storage.S3MediaStorage'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# django 3.2 버전으로 올라오면서 기본키 유형을 사용자가 정의 할 수 있게 되었음(AutoField, Big AutoField 등)
# 정의하지 않아도 문제는 없지만 Warning 발생함
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        # ---------------------------------- [edit] ---------------------------------- #
        'standard': {
            'format': str(timezone.localtime()) + ' [%(levelname)s] %(name)s: %(message)s'
        },
        # ---------------------------------------------------------------------------- #
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        # ---------------------------------- [edit] ---------------------------------- #
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/logs/'
                        + str(timezone.localtime().year)
                        + str(timezone.localtime().month)
                        + str(timezone.localtime().day)
                        + '.log',
            'maxBytes': 1024 * 1024 * 10,  # 5 MB
            'backupCount': 31,
            'formatter': 'standard',
        },
        # ---------------------------------------------------------------------------- #
    },
    'loggers': {
        'django': {
            # ---------------------------------- [edit] ---------------------------------- #
            'handlers': ['console', 'mail_admins', 'file'],
            # ---------------------------------------------------------------------------- #
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     # id나 email과 비슷한지 체크
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        # 최소 몇글자
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    # {
    #     # 사람들이 일반적으로 사용하는 비번 block ex)asdf
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        # 전부 숫자인 비번은 막음
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'magazine.User'

# EMAIL authentication
EMAIL_HOST = get_secret("EMAIL")['EMAIL_HOST']
# 메일을 호스트하는 서버
EMAIL_PORT = get_secret("EMAIL")['EMAIL_PORT']
# gmail과의 통신하는 포트
EMAIL_HOST_USER = get_secret("EMAIL")['EMAIL_HOST_USER']
# 발신할 이메일
EMAIL_HOST_PASSWORD = get_secret("EMAIL")['EMAIL_HOST_PASSWORD']
# 발신할 메일의 비밀번호
EMAIL_USE_TLS = True
# TLS 보안 방법
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER