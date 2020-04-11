from .base import *
# from .db_routers import ChinookRouter
DEBUG = True
import json
ALLOWED_HOSTS = ['*']

arrayPath=(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
fileConfig = arrayPath+'/config/develop.json'
with open(fileConfig) as data_file:    
    dataConfig = json.load(data_file)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': dataConfig.get('mongo-connection').get('database_name'),
#         'HOST': dataConfig.get('mongo-connection').get('host'),
#         'PORT': dataConfig.get('mongo-connection').get('port'),
#         'USER': dataConfig.get('mongo-connection').get('user'),
#         'PASSWORD': dataConfig.get('mongo-connection').get('password')
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = dataConfig.get('secret_key').get('key')
# Api CovidNet Peru
COVIDNET_ENDPOINT = dataConfig.get('api_diagnosis_covid19').get('covidnet_endpoint')
COVIDNET_API_KEY = dataConfig.get('api_diagnosis_covid19').get('covidnet_apikey')

# Email server
EMAIL_BACKEND = dataConfig.get("email_server").get("email_backend")
EMAIL_SITE = dataConfig.get("email_server").get("email_site")
EMAIL_USE_TLS = dataConfig.get("email_server").get("email_use_tls")
DEFAULT_FROM_EMAIL = dataConfig.get("email_server").get("default_from_email")
SERVER_EMAIL = dataConfig.get("email_server").get("server_email")
EMAIL_HOST = dataConfig.get("email_server").get("email_host")
EMAIL_PORT = dataConfig.get("email_server").get("email_port")
EMAIL_HOST_USER = dataConfig.get("email_server").get("email_host_user")
EMAIL_HOST_PASSWORD = dataConfig.get("email_server").get("email_host_password")