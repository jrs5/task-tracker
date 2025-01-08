import os
from enum import StrEnum
from functools import cache
from pathlib import Path

import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv.load_dotenv()


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    aws_region: str
    db_table: str
    environment: str
    log_level: LogLevel


def load_configuration(
    env_file_path: Path = Path(os.environ.get("ENV_FILE_LOCATION", "/opt/.env")),
) -> ServiceSettings:
    return ServiceSettings(_env_file=env_file_path)


@cache
def get_config() -> ServiceSettings:
    """
    Returns the configuration for the service.
    """

    return load_configuration()
