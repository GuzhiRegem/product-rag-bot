import unittest
from engine.embedding import EmbeddingClient
from engine.environment import Environment
from engine.agent import Agent
from engine.db import DB
from populate_db import populate


class TestEmbeddingClient(unittest.TestCase):
    def setUp(self):
        self.embedding_client = EmbeddingClient(Environment.EMBEDDING_MODEL)

    def test_generate_embedding(self):
        text = "This is a test."
        embedding = self.embedding_client.embed(text)
        self.assertIsInstance(embedding, list)
        self.assertGreater(len(embedding), 0)

    def test_embedding_consistency(self):
        text = "This is a test."
        embedding1 = self.embedding_client.embed(text)
        embedding2 = self.embedding_client.embed(text)
        self.assertEqual(embedding1, embedding2)


class TestDB(unittest.TestCase):
    def setUp(self):
        self.db = DB()
        populate(self.db)

    def test_all_products(self):
        products = self.db.all()
        self.assertGreater(len(products), 7)

    def test_add_product(self):
        product = {
            "name": "Test Product",
            "description": "This is a test product.",
            "price": 9.99,
            "category": "Test Category"
        }
        added_product = self.db.add(product)
        self.assertIn(added_product.id, [p.id for p in self.db.all()])


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.db = DB()
        populate(self.db)
        self.agent = Agent(self.db)

    def test_search_products_tool(self):
        product = self.db.all()[-1]
        result = self.agent.search_products_tool(product.name)
        self.assertIn(product.id, result)

    def test_get_product_tool(self):
        product_id = self.db.all()[0].id
        result = self.agent.get_product_tool(product_id)
        self.assertIn(product_id, result)
