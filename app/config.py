import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration settings.
    """
    APP_NAME: str = "Rolex Price API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "Production-ready FastAPI REST API providing access to Rolex watch "
        "catalog, retail pricing, collections breakdown, search, and statistics."
    )
    
    # Data source path with fallbacks
    DATA_PATH: Path = Path("data/rolex_watches.json")
    
    # Pagination defaults
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # API Documentation URLs
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"

    model_config = SettingsConfigDict(
        env_prefix="ROLEX_",
        case_sensitive=False,
        extra="ignore",
    )

    def resolve_data_path(self) -> Path:
        """
        Resolves the actual JSON data file path, checking fallbacks if primary path does not exist.
        """
        if self.DATA_PATH.exists():
            return self.DATA_PATH
        
        fallback_paths = [
            Path("data/Rolex_retail_original.json"),
            Path("Rolex_retail_original.json"),
        ]
        
        for path in fallback_paths:
            if path.exists():
                return path
                
        raise FileNotFoundError(
            f"Rolex data file not found at {self.DATA_PATH} or any fallback location."
        )


settings = Settings()
