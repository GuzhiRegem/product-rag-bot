import os
from dotenv import load_dotenv
from pydantic import SecretStr
load_dotenv()


def secure_getenv(key: str) -> str:
    """Ensure that an environment variable is set and return its value."""
    value = os.getenv(key, None)
    if value is None:
        raise ValueError(f"Environment variable '{key}' is not set.")
    return value


class Environment:
    """
    A class to manage environment variables for the application.
    """
    TOPK: int = int(secure_getenv("TOPK"))
    EMBEDDING_MODEL = secure_getenv("EMBEDDING-MODEL")
    GROQ_API_KEY = SecretStr(secure_getenv("GROQ-API-KEY"))
    GROQ_MODEL = secure_getenv("GROQ-MODEL")
