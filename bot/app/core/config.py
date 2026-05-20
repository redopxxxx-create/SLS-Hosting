from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    bot_owner_id: int = 0
    admin_ids: str = ""
    mongo_uri: str = "mongodb://localhost:27017"
    db_name: str = "sls_hosting"
    bot_api_base: str = "http://localhost:8000"
    upload_root: str = "./storage"
    max_file_size_mb: int = 100
    join_channels: str = ""
    support_channel: str = "https://t.me/+yuLoicn7Djk0ZDY1"
    powered_by_text: str = "Powered by SLS BOTS"
    restart_interval_hours: int = 24
    developer_name: str = "@ItsRyoSudhish"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def admin_id_list(self) -> set[int]:
        raw = [x.strip() for x in self.admin_ids.split(",") if x.strip()]
        return {int(x) for x in raw if x.isdigit()}


@lru_cache
def get_settings() -> Settings:
    return Settings()
