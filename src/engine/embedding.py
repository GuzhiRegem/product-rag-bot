from engine.singleton import Singleton
from sentence_transformers import SentenceTransformer


class EmbeddingClient(metaclass=Singleton):
    """A client for generating embeddings using a specified model."""
    def __init__(
        self,
        embedding_model: str
    ) -> None:
        print("Loading embedding model")
        try:
            self.__model = SentenceTransformer(
                model_name_or_path=embedding_model
            )
            print("Embedding model loaded")
        except Exception as e:
            raise ValueError(
                f"Failed to load embedding model '{embedding_model}': {e}"
            )

    def embed(
        self,
        text: str
    ) -> list[float]:
        res = self.__model.encode([text])[0].tolist()
        return res
