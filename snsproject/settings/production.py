from .base import *
import dj_database_url


SECRET_KEY = os.environ.get('SECRET_KEY')

NEWS_API = os.environ.get('NEWS_API')

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','.herokuapp.com']

db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)