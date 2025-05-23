from .base import *
import dj_database_url

# Create CSRF_TRUSTED_ORIGINS env variable with onrender.com domain name
CSRF_TRUSTED_ORIGINS = [config('CSRF_TRUSTED_ORIGINS')]

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:postgres@localhost:5432/postgres',
        conn_max_age=600
    )
}

# Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
# and renames the files with unique names for each version to support long-term caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'