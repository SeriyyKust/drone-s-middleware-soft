from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".db.env", env_file_encoding="utf-8")
    sqlite_db: str = Field(min_length=1)


db_settings = DBSettings()
