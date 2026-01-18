import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    """Central configuration loader."""

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    @classmethod
    def validate(cls):
        """Ensure critical variables are set."""
        missing = []
        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if not cls.GITHUB_TOKEN:
            missing.append("GITHUB_TOKEN")

        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")


# Validate on import (fail fast)
Config.validate()
