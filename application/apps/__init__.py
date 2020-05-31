"""Flask initialization"""

from flask import (Flask, request, jsonify)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from werkzeug.exceptions import NotFound

from source.loggers import logger

# Database variable for connection
application = Flask(__name__)
cors = CORS(application)
database = SQLAlchemy()


def create_app(config, drop_tables: bool = False) -> Flask:
    # Create a flask application
    application.config.from_object(config)
    # Initialize the database connection within an application
    database.init_app(app=application)
    from .youtube_scraper.models import (Result, ScraperResultChange)

    if drop_tables:
        with application.app_context():
            database.drop_all()
            database.create_all()

    from .youtube_scraper import youtube_scraper

    application.register_blueprint(youtube_scraper)

    return application


@application.errorhandler(500)
def error_500(error):
    logger.error(f'{request.url} {str(error)}')
    return jsonify({'data': f'server error: {request.url}'}), 500


@application.errorhandler(404)
def error_404(error: NotFound):
    logger.error(f'{request.url} {str(error)}')
    return jsonify({'data': f'page not found: {request.url}'}), 404
