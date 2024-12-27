import logging
import os
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self):
        self.logger = None

    def init_app(self, app):
        log_level = app.config.get("LOG_LEVEL", "INFO")

        if not os.path.exists("logs"):
            os.makedirs("logs")

        file_handler = RotatingFileHandler(
            "logs/app.log", maxBytes=10240, backupCount=10
        )
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.getLevelName(log_level))

        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.getLevelName(log_level))
        self.logger = app.logger


logger = Logger()
