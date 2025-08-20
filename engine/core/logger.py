# app/core/logger.py

import logging
from logging.handlers import RotatingFileHandler
import os

from engine.core.config import settings

LOG_DIR = settings.LOG_DIR

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

# File Handler (rotates after 5MB, keeps 5 backups)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5)
file_handler.setFormatter(formatter)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Logger
logger = logging.getLogger("copilot-backend")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.propagate = False  # avoid duplicate logs
