from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gd)b6%djxlp0g1zw#@5v3_w#d%pu4%g7)-!288)@m(1kz*w+n6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['79.175.177.113']

APP_NAME = 'backboiler'
APP_URL = 'http://127.0.0.1:8000'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_spectacular',
    'corsheaders',
    'rest_framework',
    'tailwind',
    'theme',
    'django_browser_reload',
    'ConnectModel',
    'LogModel',
    'UserModel',
    'AuthModel', 
    'working_noban_data',   
]

# CORS Headers
CORS_ORIGIN_ALLOW_ALL = False  # Change to True to disable CORS entirely
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:3004',
    
    'http://localhost',
    'http://79.175.177.113:16300',
    'http://192.168.15.221',  # Added this IP
]
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:3004',
    
    'http://localhost',
    'http://192.168.15.221',  # Added this IP
]
CORS_ALLOW_HEADERS = [
    "accept", "referer", "accept-encoding", "authorization",
    "content-type", "dnt", "origin", "user-agent", "x-csrftoken",
    "x-sessionid", "x-requested-with"
]
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'OPTIONS',
]
CORS_ALLOW_CREDENTIALS = True

# Uncomment the following to disable CORS entirely
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = []  # Empty the list

# Tailwind Settings
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]
# NPM_BIN_PATH = 'C:/Program Files/nodejs/npm.cmd'
from .app_lib import Find_npm_bin
NPM_BIN_PATH = Find_npm_bin()
#####

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    'LogModel.log_handler.drf_ExceptionMiddleware',
]
# settings.py
DISABLE_LOG = True  # Set this to True to disable logging


ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dbs/') + 'main.sqlite3',
    },
    'Logs': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dbs/') + 'Logs.sqlite3',
    },
    'nobaan': {  # New MySQL database (read-only)
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'salamdocto_nobaan',
        'USER': 'readonlyuser',
        'PASSWORD': 'Eh#k8X2qd629',
        'HOST': '185.252.29.25',
        'PORT': 8080,
        'OPTIONS': {
            
            'ssl': {'ssl-mode': 'disabled'},
            'charset': 'utf8mb4',  # Or use a compatible charset like utf8 if necessary.
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';"
            # 'init_command': "SET SESSION TRANSACTION READ ONLY",
        },
    },
}

AUTH_USER_MODEL = 'UserModel.User'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'custom_exception_handler.no_logging_exception_handler',
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Nobaan API',
    'DESCRIPTION': 'API for nobaan database',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'PREPROCESSING_HOOKS': ['app.swagger_schema.preprocessing_filter_spec']
}

# In your settings.py (or a dedicated router file)
class ReadOnlyRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'nobaan':
            # Skip migrations for the read-only nobaan database.
            return False
        # Allow migrations for all other databases.
        return None

DATABASE_ROUTERS = ['app.settings.ReadOnlyRouter']
