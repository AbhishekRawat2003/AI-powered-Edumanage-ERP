from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-$djeoy5v6ak1z)3%i%aw1nts=x8!x@r%)b8lj(klmdpz90d8n('


DEBUG = True

ALLOWED_HOSTS = []



INSTALLED_APPS = [
    # 'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'EduManage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [os.path.join(BASE_DIR, 'templates')],
        'DIRS': [BASE_DIR / 'templates',
            BASE_DIR / 'student/templates',  # Add paths for each app's templates folder
            BASE_DIR / 'faculty/templates',],
        # 'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'EduManage.wsgi.application'

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

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]


# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# << Custom >>

EXTERNAL_APPS=[
    'student',
    'faculty',
    'course',
    'attendance',
    'authentication',
]

INSTALLED_APPS  += EXTERNAL_APPS

JAZZMIN_SETTINGS = {
    "site_title": "EdiManage",
    "site_header": "EduManage",
    "site_brand": "Edumanage",
    "site_icon": "images/favicon.png",  # Path to your favicon
    "welcome_sign": "Welcome to My Edumanage Admin",
    "copyright": "Edumanage@2024",
}
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default backend
    'authentication.backends.EmailBackend',  # Custom email backend
]
AUTH_USER_MODEL = 'authentication.CustomUser'

LOGIN_URL = '/login/'  # This refers to the name='login' in your urls.py
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')