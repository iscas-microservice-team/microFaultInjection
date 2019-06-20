import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abcdef020301abc8c86f'

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')

    # my postgres in K8s
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # K8s config
    # POSTGRES_HOST = os.environ.get('COFFEESHOP_POSTGRES_SERVICE_HOST')
    # POSTGRES_PORT = os.environ.get('COFFEESHOP_POSTGRES_SERVICE_PORT')
    # POSTGRES_DBNAME = os.environ.get('POSTGRES_DBNAME')
    # POSTGRES_USERNAME = os.environ.get('POSTGRES_USERNAME')
    # POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    # POSTGRES_PROTOCOL = os.environ.get('POSTGRES_PROTOCOL')
    # POSTGRES_SSLMODE = os.environ.get('POSTGRES_SSLMODE')
    #
    # # assembled Database URI
    # SQLALCHEMY_DATABASE_URI = POSTGRES_PROTOCOL + '://' + POSTGRES_USERNAME + ':' + POSTGRES_PASSWORD + '@' +\
    #                           POSTGRES_HOST + ':' + POSTGRES_PORT + '/' + POSTGRES_DBNAME + '?sslmode=' + POSTGRES_SSLMODE

    # protocol + `://` + dbUsername + `:` + dbPassword + `@` + dbIp + `:` + dbPort + `/` + dbName + `?sslmode=` +sslMode
    # SQLALCHEMY_DATABASE_URI = 'postgres://dbuser:love_coffee@23.106.158.242:31432/coffeeshop?sslmode=disable'

    # SQLALCHEMY_TRACK_MODIFICATIONS = False
