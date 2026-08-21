import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-jwt-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}