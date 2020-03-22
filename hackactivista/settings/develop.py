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
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': dataConfig.get('mongo-connection').get('database_name'),
        'HOST': dataConfig.get('mongo-connection').get('host'),
        'PORT': dataConfig.get('mongo-connection').get('port'),
        'USER': dataConfig.get('mongo-connection').get('user'),
        'PASSWORD': dataConfig.get('mongo-connection').get('password')
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = dataConfig.get('secret_key').get('key')
WHATSAPP_CONFIG = dataConfig.get('wsp')