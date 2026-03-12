import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")
logger.add("/var/log/btrfs-manager.log", rotation="10 MB", retention="30 days", level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}")

def get_logger():
    return logger
