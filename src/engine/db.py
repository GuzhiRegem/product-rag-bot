from typing import Optional, TypedDict, Union
from pydantic import BaseModel
from dataclasses import field
import uuid
from engine.embedding import EmbeddingClient
import numpy as np
from engine.singleton import Singleton
from engine.environment import Environment


class ProductDict(TypedDict):
    name: str
    description: str
    price: float
    category: str


class Product(BaseModel):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    category: str

    def to_text(self) -> str:
        out = "\n".join([
            f"ID: {self.id}",
            f"Name: {self.name}",
            f"Description: {self.description}",
            f"Price: ${self.price:.2f}",
            f"Category: {self.category}"
        ])
        return out


class DB(Singleton):
    def __init__(
        self,
        embedding_client: Optional[EmbeddingClient] = None
    ) -> None:
        if embedding_client is None:
            self.__embedding_client = EmbeddingClient(
                embedding_model=Environment.EMBEDDING_MODEL
            )
        else:
            self.__embedding_client = embedding_client
        self.__objects_list: list[Product] = list()
        self.__objects_map: dict[str, Product] = dict()
        self.__embedding_map: dict[str, list[float]] = dict()

    def add(self, product: Union[Product, ProductDict]) -> Product:
        created_product: Optional[Product] = None
        match product:
            case Product():
                created_product = product
            case dict():
                created_product = Product(**product)
            case _:
                raise TypeError("Invalid product")

        product_embedding = self.__embedding_client.embed(
            created_product.to_text()
        )

        self.__objects_list.append(created_product)
        self.__objects_map[created_product.id] = created_product
        self.__embedding_map[created_product.id] = product_embedding
        return created_product

    def get(self, product_id: str) -> Optional[Product]:
        return self.__objects_map.get(product_id)

    def all(self) -> list[Product]:
        return self.__objects_list

    def __cosine_similarity(
        self,
        vec_a: list[float],
        vec_b: list[float]
    ) -> float:
        """ Calculate cosine similarity between two vectors using polars. """
        v1_np = np.array(vec_a)
        v2_np = np.array(vec_b)
        dot_product = np.dot(v1_np, v2_np)
        magnitude_v1 = np.linalg.norm(v1_np)
        magnitude_v2 = np.linalg.norm(v2_np)
        if magnitude_v1 == 0 or magnitude_v2 == 0:
            return 0.0  # Handle zero vectors
        return (dot_product / (magnitude_v1 * magnitude_v2))

    def search(self, query: str, top_k: int = 10) -> list[Product]:
        scores: list[tuple[str, float]] = []
        query_embedding = self.__embedding_client.embed(query)
        for product_id, embedding in self.__embedding_map.items():
            score = self.__cosine_similarity(query_embedding, embedding)
            scores.append((product_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        top_scores = scores[:top_k]
        return [self.__objects_map[product_id] for product_id, _ in top_scores]
