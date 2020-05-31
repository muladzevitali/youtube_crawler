import logging

from source.configuration import media_config


class FileHandlerLogger:
    logger_name = 'youtube-crawler-back'
    logger_file_info = media_config.log_file_info
    logger_file_error = media_config.log_file_error
    logger_format = logging.Formatter(fmt='%(asctime)s :: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    def __init__(self):
        self.log = logging.getLogger(self.logger_name)
        self.log.setLevel(logging.DEBUG)
        self.log.propagate = False
        # Info type file handler
        file_handler_info = logging.FileHandler(self.logger_file_info, mode='a', encoding='utf-8')
        file_handler_info.setFormatter(self.logger_format)
        file_handler_info.setLevel(logging.INFO)
        self.log.addHandler(file_handler_info)

        # Error type file handler
        file_handler_error = logging.FileHandler(self.logger_file_error, mode='a', encoding='utf-8')
        file_handler_error.setFormatter(self.logger_format)
        file_handler_error.setLevel(logging.ERROR)
        self.log.addHandler(file_handler_error)

    def info(self, message):
        self.log.info(message)

    def error(self, message):
        self.log.error(message)