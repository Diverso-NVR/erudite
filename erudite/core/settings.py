import typing
import logging

from pydantic import BaseSettings, Field


def create_logger(name: str, mode: str = "INFO"):
    logs = {"INFO": logging.INFO, "DEBUG": logging.DEBUG}

    logger = logging.getLogger(name)
    logger.setLevel(logs[mode])

    handler = logging.StreamHandler()
    handler.setLevel(logs[mode])

    formatter = logging.Formatter(
        "%(levelname)-8s  %(asctime)s    %(message)s", datefmt="%d-%m-%Y %I:%M:%S %p"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)


class Settings(BaseSettings):
    psql_url: str = Field(..., env="PSQL_DB_URL")
    mongo_url: str = Field(..., env="MONGO_DB_URL")

    testing: typing.Optional[bool] = Field(env="TESTING")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings(_env_file="../.env")
