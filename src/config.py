import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    DEBUG = os.environ.get('FLASK_DEBUG') or True