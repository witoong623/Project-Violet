from .settings import *


SECRET_KEY = env('PROJECT_VIOLET_SECRET', default='')

DEBUG = False

ALLOWED_HOSTS = [env('ALLOWED_HOST', default='*')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'webpack_loader',
    'rest_framework',
    'website.apps.WebsiteConfig',
    'core.apps.CoreConfig',
]

# Add debug toolbar app if debug in production
if DEBUG:
    INSTALLED_APPS = ['debug_toolbar'] + INSTALLED_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add debug toolbar middleware if debug in production
if DEBUG:
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'football_recommend',
        'USER': 'projectvioletdb',
        'PASSWORD': '123456',
        'HOST': 'db',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'projectviolet.urls_prod'

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'website/js/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats-prod.json'),
        'POLL_INTERVAL': 10,
    }
}

# Debug toolbar settings
INTERNAL_IPS = [env('INTERNAL_IPS_DEBUG', default='192.168.99.101')]
