import sys

from apps import create_app
from source.configuration import app_config
from source.loggers import logger

# To reset the whole database
drop_tables: bool = sys.argv[-1] == 'reset'
# Load the application
application = create_app(app_config, drop_tables=drop_tables)
logger.info('application created successfully')

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)
