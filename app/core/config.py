import os
import secrets
from typing import Optional, Dict, Any

from pydantic import BaseModel, field_validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseModel):
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "API Giải Quẻ Kinh Dịch")
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    
    # LLM Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
    
    @field_validator("OPENAI_API_KEY")
    def validate_openai_api_key(cls, v: str) -> str:
        if not v and os.getenv("DEBUG") != "True":
            raise ValueError("Cần phải thiết lập OPENAI_API_KEY trong môi trường sản xuất")
        return v

settings = Settings()
