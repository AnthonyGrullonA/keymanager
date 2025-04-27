import os
import environ
from pathlib import Path

# 1. Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Inicializar environment
env = environ.Env(
    DEBUG=(bool, False),
    DEV=(bool, True),
)

# 3. Leer archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# 4. Seguridad
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
DEV = env('DEV')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# 5. Cifrado
PASSWORD_ENCRYPTION_KEY = env('PASSWORD_ENCRYPTION_KEY')

# 6. Internacionalización
LANGUAGE_CODE = env('LANGUAGE_CODE', default='en-us')
TIME_ZONE = env('TIME_ZONE', default='UTC')
USE_I18N = env.bool('USE_I18N', default=True)
USE_TZ = env.bool('USE_TZ', default=True)

# 7. Static y Media
STATIC_URL = env('STATIC_URL')
MEDIA_URL = env('MEDIA_URL')

STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

# 8. Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vault',
]

# 9. Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 10. Rutas
ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# 11. Base de datos


data_path = BASE_DIR / 'data'
if not data_path.exists():
    data_path.mkdir(parents=True, exist_ok=True)
    
if DEV:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'data' / env('SQLITE_NAME'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('POSTGRES_DB'),
            'USER': env('POSTGRES_USER'),
            'PASSWORD': env('POSTGRES_PASSWORD'),
            'HOST': env('POSTGRES_HOST'),
            'PORT': env('POSTGRES_PORT'),
        }
    }
    
# 12. Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# 13. Primary key type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
