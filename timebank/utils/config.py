from datetime import timedelta


# Vytvorenie zakladnej classy config
class Config(object):
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = '71d69e882b38fa377e97affa0ad8e4875b8ea5e10e858ba54cbb79c4b0c66739'
    JWT_ACCESS_COOKIE_PATH = '/auth/'
    JWT_REFRESH_COOKIE_PATH = '/auth/refresh'
    JWT_TOKEN_LOCATION = ["cookies", "headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
    JWT_REFRESH_CSRF_HEADER_NAME = "X-CSRF-TOKEN-REFRESH"
    CORS_HEADERS = 'Content-Type'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True


# Nastavenie produkcneho configu
class ProductionConfig(Config):
    # DB_HOST = '127.0.0.1'
    DB_HOST = '157.230.79.85'
    DB_PASSWORD = "Fej1chahgheebohxohxi"
    DB_PORT = '33306'
    DB_NAME = "timebank"
    DB_USERNAME = "automation"
    DB_CHARSET = "utf8mb4"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:" \
                              f"{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"


# Nastavenie delelopment configu
class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    TESTING = True
    # DB_HOST = '127.0.0.1'
    DB_HOST = '157.245.27.101'
    DB_PASSWORD = "ue1roo0uawechai5nieg1B"
    DB_PORT = '33306'
    DB_NAME = "timebank"
    DB_USERNAME = "automation"
    DB_CHARSET = "utf8mb4"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:" \
                              f"{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"


# Nastavenie testing configu
class TestingConfig(Config):
    DB_HOST = '157.245.27.101'
    DB_PASSWORD = "ue1roo0uawechai5nieg1B"
    DB_PORT = '33306'
    DB_NAME = "timebank_testing"
    DB_USERNAME = "automation"
    DB_CHARSET = "utf8mb4"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:" \
                              f"{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"
