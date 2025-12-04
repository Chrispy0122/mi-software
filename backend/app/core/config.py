from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "CRM Backend"
    API_V1_STR: str = "/v1"
    
    # Database
    DB_HOST: str = Field(alias="HOST", default="localhost")
    DB_PORT: int = Field(alias="PORT", default=3306)
    DB_USER: str = Field(alias="USER", default="root")
    DB_PASSWORD: str = Field(alias="PASSWORD", default="") # Handling the typo in .env
    DB_NAME: str = Field(alias="DATABASE_NAME", default="crm_db")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
