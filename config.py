import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

TOKEN_ID = os.getenv('TOKEN_ID')
SUPER_ADMIN_ID = os.getenv('SUPER_ADMIN_ID')
BOT_ID = os.getenv('BOT_ID')

TOKEN_YOUKASSA = os.getenv('TOKEN_YOUKASSA')

# db_config = {
#     'HOST': os.getenv('DB_HOST'),
#     'USER': os.getenv('DB_USER'),
#     'PASS': os.getenv('DB_PASSWORD'),
#     'DB_NAME': os.getenv('DB_NAME')
# }
class Settings(BaseSettings):
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DB_NAME: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    ENGINE: str | None = None
    SQL_DB: str | None = None

    MEDIA: str | None = None
    MEDIA_TMP: str | None = None

    path_env: str = str(Path(__file__).resolve().parent)
    model_config = SettingsConfigDict(enf_file=f"{path_env}/.env")

    @property
    def connect_url(self):
        if self.SQL_DB:
            return self.SQL_DB
        else:
            return f'{self.ENGINE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'




settings = Settings()

