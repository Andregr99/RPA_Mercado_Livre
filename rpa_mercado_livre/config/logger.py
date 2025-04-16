from rich.logging import RichHandler
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    handlers=[RichHandler()]
)

logger = logging.getLogger("rich")

def log_error(error):
    logger.error(f"Error no processo principal: {str(error)}")