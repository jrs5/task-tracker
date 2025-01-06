from aws_lambda_powertools import Logger

from .config import get_config

config = get_config()
logger: Logger = Logger(level=config.log_level)
