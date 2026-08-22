import os
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Settings:
    virtual_path: str = field(default=Path(r"E:\workspace\temp\virtual"))
    api_key: str = field(default=os.getenv("API_KEY", "qwen3.6:35b"))
    base_url: str = field(default=os.getenv("BASE_URL", ""))
    model: str = field(default=os.getenv("MODEL", ""))
    embedding_api_key: str = field(default=os.getenv("API_KEY", ""))
    embedding_base_url: str = field(default=os.getenv("BASE_URL", ""))
    embedding_model: str = field(default=os.getenv("EMBEDDING_MODEL", ""))


settings = Settings()
