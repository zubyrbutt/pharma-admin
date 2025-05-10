import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_super_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    API_TITLE = os.getenv('API_TITLE', 'Advanced Flask API')
    API_VERSION = os.getenv('API_VERSION', '1.0')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///instance/dev.db')


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Use persistent disk on Render if available, otherwise use instance directory
    if os.getenv('RENDER'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:////data/production.db')
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///instance/production.db')


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 