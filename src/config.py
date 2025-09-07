import os


class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    DEBUG = True
    # PostgreSQL configuration for Replit
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@helium/heliumdb?sslmode=disable')


config = {
    'DevelopmentConfig': DevelopmentConfig
}

