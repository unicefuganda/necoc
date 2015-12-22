# Django settings for necoc project.
import mongoengine
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

here = lambda * x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda * x: os.path.join(os.path.abspath(PROJECT_ROOT), *x)


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

API_TOKEN = os.environ['API_TOKEN']
API_AUTHORIZED_STEP = os.environ['API_AUTHORIZED_STEP']
API_URL = 'https://app.rapidpro.io/api/v1/sms.json'
LOCATION_MATCH_LEVEL = 0.9
MESSAGE_LOCATION_INDEX = 2
POLL_RESPONSE_KEYWORD_INDEX = 2
ALWAYS_OPEN_POLLS = 3
POLL_RESPONSE_SEPARATORS = [' ','.']
MESSAGE_SEPARATOR = '.'
INTERNATIONAL_PHONE_PREFIX = '+'
DEFAULT_STR_MATCH_RATIO = 90 #expressed in absolute percentange values
DISASTER_STATUSES = ['Registered', 'Situation Report Field', 'Verification', 'Assessment', 'Deployed Response Team', 'Closed']
DISASTER_ASSOCIATION_MATCH_RATIO = 50 #Expressed in absolute percentage value
COUNTRY_CALLING_CODE = 256
NUMBER_OF_CHARS_IN_PHONE_NUMBER = 9 #Without country code and leading zero(s)

# accepted yes keywords
YES_WORDS = ['yes', 'yeah', 'yep', 'yay', 'y']

# accepted no keywords
NO_WORDS = ['no', 'nope', 'nah', 'nay', 'n']

# Poll Response Evaluation Templates
# The standard template allows for any amount of whitespace at the beginning,
# followed by the alias(es) for a particular category, followed by any non-
# alphabetical character, or the end of the message
STARTSWITH_PATTERN_TEMPLATE = '^\s*(%s)(\s|[^a-zA-Z]|$)'
CONTAINS_PATTERN_TEMPLATE = '^.*\s*(%s)(\s|[^a-zA-Z]|$)'
DEFAULT_POLL_RESPONSE = (True, 'Thank you for your response')
POLL_RESPONSE_START_STR = 'NECOCPoll'



MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': '',
    }
}

SESSION_ENGINE = 'mongoengine.django.sessions'

MONGODB_USER = ''
MONGODB_PASSWORD = ''
MONGODB_HOST = 'localhost'
MONGODB_NAME = 'dms'
MONGODB_DATABASE_HOST = 'mongodb://%s/%s' % (MONGODB_HOST, MONGODB_NAME)

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Africa/Nairobi'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your client files
# in apps' "client/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/static'

# URL prefix for client files.
# Example: "http://example.com/static/", "http://client.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    root("..", "dms/client/app"),
    # Put strings here, like "/home/html/client" or "C:/www/django/client".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find client files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+#8&t7(+xx5lo%p%(^$8!!)awz11dy(9o!#8ksie@p9i#lb-34'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'necoc.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'necoc.wsgi.application'

TEMPLATE_DIRS = (
    root("..", "dms/templates"),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)


DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)


THIRD_PARTY_APPS = (
    'rest_framework',
    'djcelery',
    'mongoengine.django.mongo_auth',
    'imagekit',
    'django_extensions',
)

LOCAL_APPS = (
    'dms',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.SessionAuthentication',
       'dms.services.token_authentication.TokenAuth',
       'rest_framework.authentication.BasicAuthentication',
       'dms.utils.internal_auth.InternalCallAuth',
   ),

   'DEFAULT_PERMISSION_CLASSES': (
       'rest_framework.permissions.IsAuthenticated',
   ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_csv.renderers.CSVRenderer'
    ),

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework_csv.parsers.CSVParser',
    ),

    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    )
}

AUTH_USER_MODEL = 'mongo_auth.MongoUser'
MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'necocdev@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
DEFAULT_FROM_EMAIL = 'necocdev@gmail.com'
SERVER_EMAIL = 'necocdev@gmail.com'
DEFAULT_TO_EMAIL = 'necocdev@gmail.com'
ADMIN_EMAIL = ''

HOSTNAME = 'http://necoc.org.ug'

NEW_USER_MESSAGE = """
                Dear %(name)s,

                Your email was recently registered for NECOC DMS.
                Please use the following credentials to login to %(hostname)s

                username: %(username)s
                password: %(password)s

                Thank you,
                NECOC DMS team
                """

CHANGE_PASSWD_MESSAGE = """
                Dear %(name)s,

                This is to notify you that you have recently changed your password for NECOC DMS.
                You will need to use the new password to login to %(hostname)s.

                If you think this is a mistake, please contact immediately the NECOC DMS
                administrator in %(admin_email)s.

                Thank you,
                NECOC DMS team
                """

RESET_PASSWORD_MESSAGE = """
                Dear %(name)s,

                This is to notify you that your password for NECOC DMS was recently reset to:

                        password: %(password)s

                You will need to use the new password to login to %(hostname)s.

                If you think this is a mistake, please contact immediately the NECOC DMS
                administrator in %(admin_email)s.

                Thank you,
                NECOC DMS team
                """
AUTO_RESPONSE_MESSAGE = """Thank you for your message. A response team will be deployed to your area. \
Please continue sending messages using NECOC.District.Subcounty.Message to 6700
"""
# AUTO_RESPONSE_ENDPOINT = '/api/v1/sent-messages/'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
# TEST_RUNNER = 'dms.tests.runner.NoSQLTestRunner'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
