import os
from dotenv import load_dotenv

# Load variables from .env file into environment variables
load_dotenv()

class Settings:
    """Loads application settings from environment variables."""
    LLM_API_KEY: str = os.getenv("LLM_API_KEY")
    # Default model if not specified in .env
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "gpt-4-turbo-preview")

    # Basic check on startup to ensure the key is present
    if not LLM_API_KEY:
        raise ValueError("LLM_API_KEY environment variable not set. Please create a .env file with LLM_API_KEY=your_key")

# Create a single instance of settings to be imported elsewhere
settings = Settings()
