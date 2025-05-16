from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

logger.add(
    "logs/info.log",
    level=os.getenv("LOG_LEVEL", "INFO"),
    rotation="10MB",
    format="{time} - {name} - {level} - {message}",
)