# product-rag-bot

This is a quick demo for an agent that can interact with a DB of products.

### Agent Tools

- search_products: Search `top_k: int` products given a search query
- all_items: Retrieve all products
- get_product: Retrieves information about a specific product

### Models:

```
Product:
    name: str
    description: str
    price: float
    category: str
```

### Endpoints

- POST /query {"user_id": str, "query": str} -> returns answer from the assistant
- GET /all_products -> returns complete list of products

### Running

To run, copy the `env` file into a `.env` file.
This uses local embeddings models and groq for LLM inference, you'll need to set your key in the env var `GROQ-API-KEY`.

With this configured you'll need to run:
```docker compose up```

Warning: This will take a while, given that it's downloading the embedding model inside of the container. The final size of the container is 9.57GB