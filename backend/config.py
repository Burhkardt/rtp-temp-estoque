from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LOCAL_DATABASE_URL: str = "sqlite:///./local.db"
    REMOTE_DATABASE_URL: str = "sqlite:///./remote.db"
    
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
