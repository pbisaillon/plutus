from typing import Any, Callable, Set

from pydantic import (
    AliasChoices,
    AmqpDsn,
    BaseModel,
    Field,
    ImportString,
    FileUrl,
)

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sqlite_dsn: str = "sqlite:////Users/phil/Documents/repo/plutus/plutus.sqlite3"

    # to override domains:
    # export my_prefix_domains='["foo.com", "bar.com"]'
    domains: Set[str] = set()

    # to override more_settings:
    # export my_prefix_more_settings='{"foo": "x", "apple": 1}'
    model_config = SettingsConfigDict(env_prefix="my_prefix_")
