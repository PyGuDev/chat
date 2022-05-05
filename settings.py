import os

from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 8000
REFRESH_TOKEN_EXPIRE_MINUTES = 8000

USER_ID_FIELD = 'uid'
USER_USERNAME_FIELD = 'phone'

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASS = os.getenv('REDIS_PASS')
