import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration settings for the AI Research Assistant.
    Supports both OpenAI and Groq backends.
    """

    # === OpenAI Configuration ===
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))

    # === Groq Configuration ===
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    # === Application Settings ===
    APP_TITLE = "🔬 AI Research Assistant"
    APP_DESCRIPTION = "A Multi-Agent System for Comprehensive Research and Analysis"
    
    # === Agent Configuration ===
    AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "30"))  # seconds
    MAX_RESEARCH_HISTORY = int(os.getenv("MAX_RESEARCH_HISTORY", "10"))
    
    # === UI Configuration ===
    DEFAULT_EXPANDED_SECTIONS = os.getenv("DEFAULT_EXPANDED_SECTIONS", "information").split(",")

    @classmethod
    def validate_config(cls):
        """
        Validate that at least one API key is provided (OpenAI or Groq).
        """
        if not cls.OPENAI_API_KEY and not cls.GROQ_API_KEY:
            raise ValueError("❌ No API key found! Please set either OPENAI_API_KEY or GROQ_API_KEY in your .env file.")
        return True
