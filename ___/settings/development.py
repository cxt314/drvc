from .base import *

if 'CODESPACE_NAME' in os.environ:
    codespace_name = config("CODESPACE_NAME")
    codespace_domain = config("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
    CSRF_TRUSTED_ORIGINS = [f'https://{codespace_name}-8000.{codespace_domain}']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# To use sqllite as the database engine,
#   uncomment the following block and comment out the Postgres section below
#DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": BASE_DIR / "db.sqlite3",
#    }
#}

# Configure Postgres database for local development
#   Set these environment variables in the .env file for this project.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_DATABASE'),
        'HOST': config('DB_HOST'),
        'USER': config('DB_USERNAME'),
        'PASSWORD': config('DB_PASSWORD'),
    },
    'test': {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test.sqlite3",
    }
}

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",  # Default Django dev server
    "http://127.0.0.1:8000",  # Alternative local address
]