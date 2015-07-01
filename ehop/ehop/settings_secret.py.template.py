DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('admin', 'admin@mail.com')
)

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'DBname',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'DBuser',
        'PASSWORD': 'DBpassword',
        'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

#configuration de l'adresse mail noreply pour les mails automatique :
EMAIL_USE_TLS = False
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
if DEBUG:
    EMAIL_CONTACT = ADMINS[1]
else:
    EMAIL_CONTACT = 'contact@mail.com'
EMAIL_HOST_USER = 'noreply@mail.com'
EMAIL_HOST_PASSWORD = 'MAILpassword'
EMAIL_HOST = 'ssl0.ovh.net'
EMAIL_PORT = 25

#Config OVH SMS
APP_KEY = "APP_KEY"
APP_SEC = "APP_SEC"
CONS_KEY = "CONS_KEY"
SERVICE_NAME = "SERVICE_NAME"

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["DOMAIN-NAME", ".localhost"]

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'DJANGO_SECRET_KEY'