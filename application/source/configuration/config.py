"""Configuration class for applications"""

import configparser
import os

# Read the config file
config = configparser.ConfigParser()
config.read("config.ini")


class Database:
    """Configuration class for postgres databases"""

    user = config["DATABASE"]["USER"]
    password = config["DATABASE"]["PASSWORD"]
    name = config["DATABASE"]["DATABASE"]
    host = os.getenv('DATABASE', config["DATABASE"]["HOST"])
    port = config["DATABASE"]["PORT"]
    uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


class Application:
    """Configuration class for an application"""
    SECRET_KEY = config["APPLICATION"]["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = config["APPLICATION"]["SQLALCHEMY_TRACK_MODIFICATIONS"] == "true"
    SQLALCHEMY_ECHO = config["APPLICATION"]["SQLALCHEMY_ECHO"] == "true"
    SQLALCHEMY_DATABASE_URI = Database.uri
    WTF_CSRF_SECRET_KEY = "secret_word"
    SPOTIFY_CLIENT_ID = config['SPOTIFY']['CLIENT_ID']
    SPOTIFY_CLIENT_SECRET = config['SPOTIFY']['CLIENT_SECRET']
    CORS_HEADERS = 'Content-Type'

    @staticmethod
    def init_app(app):
        pass


class Media:
    """Configuration class for files"""
    media_path = config["FILES"]["MEDIA_PATH"]
    log_file_info = config["LOGGER"]["LOG_FILE_INFO"]
    log_file_error = config["LOGGER"]["LOG_FILE_ERROR"]

    def __init__(self, *args, **kwargs):
        static_variables = [value for key, value in vars(self).items() if not (key.startswith('_') or callable(value))]
        os.makedirs(self.media_path, exist_ok=True)
        os.makedirs(os.path.join(self.media_path, 'logs'), exist_ok=True)


proxies = {'http': 'http://lum-customer-hl_cd462c02-zone-static:afcf8w8d63n9@zproxy.lum-superproxy.io:22225',
           'https': 'http://lum-customer-hl_cd462c02-zone-static:afcf8w8d63n9@zproxy.lum-superproxy.io:22225'}
