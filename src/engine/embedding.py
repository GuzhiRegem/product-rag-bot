from engine.singleton import Singleton
from sentence_transformers import SentenceTransformer


class EmbeddingClient(metaclass=Singleton):
    """A client for generating embeddings using a specified model."""
    def __init__(
        self,
        embedding_model: str
    ) -> None:
        print("Loading embedding model")
        self.__model = SentenceTransformer(embedding_model)
        print("Embedding model loaded")

    def embed(
        self,
        text: str
    ) -> list[float]:
        res = self.__model.encode([text])[0]
        return res
