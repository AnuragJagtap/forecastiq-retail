import logging
import os

def get_logger(name: str):

    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)

    if not logger.handlers:

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(
            "logs/project.log"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger