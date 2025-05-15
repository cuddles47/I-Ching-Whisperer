import os
import secrets
from typing import Optional, Dict, Any, Literal, Union

from pydantic import BaseModel, field_validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseModel):
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "API Giải Quẻ Kinh Dịch")
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    
    # LLM Configuration
    LLM_PROVIDER: Literal["openai", "huggingface"] = os.getenv("LLM_PROVIDER", "huggingface")
    LLM_OPTIMIZE: bool = os.getenv("LLM_OPTIMIZE", "True") == "True"  # Whether to use optimizations
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4")
    
    # Hugging Face Configuration
    HF_MODEL_NAME: str = os.getenv("HF_MODEL_NAME", "microsoft/phi-2")
    HF_DEVICE: Optional[str] = os.getenv("HF_DEVICE", None)  # None for auto-detect
    HF_MAX_LENGTH: int = int(os.getenv("HF_MAX_LENGTH", "2048"))
    HF_MAX_NEW_TOKENS: int = int(os.getenv("HF_MAX_NEW_TOKENS", "1024"))  # Số lượng token mới tối đa
    HF_TEMPERATURE: float = float(os.getenv("HF_TEMPERATURE", "0.7"))
    HF_TOP_P: float = float(os.getenv("HF_TOP_P", "0.9"))
    
    # Optimization settings
    HF_USE_BETTER_TRANSFORMER: bool = os.getenv("HF_USE_BETTER_TRANSFORMER", "True") == "True"
    HF_USE_FLASH_ATTENTION: bool = os.getenv("HF_USE_FLASH_ATTENTION", "True") == "True"
    HF_USE_8BIT: bool = os.getenv("HF_USE_8BIT", "True") == "True"
    HF_USE_4BIT: bool = os.getenv("HF_USE_4BIT", "False") == "True"  # More aggressive quantization
    HF_BATCH_SIZE: int = int(os.getenv("HF_BATCH_SIZE", "1"))  # For batch processing
    
    @field_validator("OPENAI_API_KEY")
    def validate_openai_api_key(cls, v: str, info) -> str:
        # Only validate if using OpenAI
        values = info.data
        if values.get("LLM_PROVIDER") == "openai" and not v and os.getenv("DEBUG") != "True":
            raise ValueError("Cần phải thiết lập OPENAI_API_KEY khi sử dụng OpenAI trong môi trường sản xuất")
        return v

settings = Settings()
