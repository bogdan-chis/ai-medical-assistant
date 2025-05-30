# backend/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # RAG LLM configuration
    LLM_API_BASE_URL: str
    LLM_API_KEY: str
    LLM_MAIN_MODEL: str

    # Judge LLM configuration
    JUDGE_API_BASE_URL: str
    JUDGE_API_KEY: str
    JUDGE_MODEL_PATH: str

    # DeepEval evaluation settings
    JUDGE_METRICS: list[str] = ["faithfulness", "toxicity"]
    HALLUCI_THRESHOLD: float = 0.75
    TOXICITY_THRESHOLD: float = 0.5

    # Instruct Pydantic to load from .env
    model_config = SettingsConfigDict(
        env_file=".env"
    )
