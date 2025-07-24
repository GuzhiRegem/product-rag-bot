from engine.singleton import Singleton
from sentence_transformers import SentenceTransformer


class EmbeddingClient(Singleton):
    def __init__(
        self,
        embedding_model: str
    ) -> None:
        print("loading model")
        self.__model = SentenceTransformer(embedding_model)
        print("model loaded")

    def embed(
        self,
        text: str
    ) -> list[float]:
        res = self.__model.encode([text])[0]
        return res
