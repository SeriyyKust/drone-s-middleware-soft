from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    webserver_api_key: str = Field(min_length=32)
    probability_success_command: float = Field(ge=0.0, le=1.0)
    base_url: str = Field(min_length=1)
    bot_token: str = Field(min_length=1)

    redis_url: str = Field(min_length=1)
    redis_host: str = Field(min_length=1)
    redis_port: int = Field()

    ws_server_notification_telegram: bool = Field(default=False)

    def get_webhook_url(self) -> str:
        return f"{self.base_url}/telegram/test/webhook"


app_config = AppConfig()
