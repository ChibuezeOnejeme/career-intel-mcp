from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./career_intel.db"
    llm_api_key: str = ""
    llm_model: str = "deepseek/deepseek-chat"
    llm_base_url: str = "https://openrouter.ai/api/v1"
    api_key: str = "career-mcp-dev-key"
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
