import logging
import os

import dotenv

dotenv.load_dotenv()

logging.basicConfig(level=os.getenv("LOG_LEVEL", "WARNING").upper())
