class Configuration(object):
    DEBUG = True
    SECRET_KEY = 'wadqwqwrqvwteltw[wr[qq'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/db2'
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_COOKIE_PATH = '/'
