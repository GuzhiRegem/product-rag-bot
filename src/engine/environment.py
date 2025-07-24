import os
from dotenv import load_dotenv
load_dotenv()


def secure_getenv(key: str) -> str:
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
    GROQ_API_KEY = secure_getenv("GROQ-API-KEY")
    GROQ_MODEL = secure_getenv("GROQ-MODEL")
