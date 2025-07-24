from typing import Optional
from langchain_core.tools import tool
from engine.db import DB
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from engine.environment import Environment
from engine.conversation import Conversation, MessageDict


class Agent:
    def __init__(self, db: Optional[DB] = None) -> None:
        if db is not None:
            self.__db = db
        else:
            self.__db = DB()
        self.__conversation = Conversation(
            system_message="""
            You are a helpful assistant that can
            search for products in a database.
            """
        )

        @tool
        def search_products(
            query: str
        ) -> str:
            """
            Search for products based on the provided query.
            Args:
                query (str): The search query to find relevant products.
            Returns:
                str: A string representation of the search results.
            """
            return self.search_products_tool(query)

        @tool
        def all_products() -> str:
            """
            Get a list of all products in the database.
            Returns:
                str: a list of all products.
            """
            return self.all_products_tool()
        
        @tool
        def get_product(
            product_id: str
        ) -> str:
            """
            Get a specific product by its ID.
            Args:
                product_id (str): The ID of the product to retrieve.
            Returns:
                str: A string representation of the product details.
            """
            return self.get_product_tool(product_id)

        self.__graph = create_react_agent(
            ChatGroq(
                model=Environment.GROQ_MODEL,
                api_key=Environment.GROQ_API_KEY
            ),
            tools=[search_products, all_products, get_product]
        )

    def search_products_tool(
        self,
        query: str
    ) -> str:
        top_k = Environment.TOPK
        products = self.__db.search(query, top_k=top_k)
        out = f"""
        Query: '{query}'
        Top-K: {top_k}
        Results: [
        """
        for product in products:
            out += f"\n{product.to_text()}\n"
        out += "]"
        return out

    def get_product_tool(
        self,
        product_id: str
    ) -> str:
        product = self.__db.get(product_id)
        return product.to_text() if product else "Product not found."

    def all_products_tool(
        self
    ) -> str:
        products = self.__db.all()
        out = "["
        for product in products:
            out += f"\n{product.id}.{product.category}.{product.name}\n"
        out += "] length: " + str(len(products))
        return out

    def send_message(
        self,
        content: str
    ) -> MessageDict:
        self.__conversation.add("user", content)
        graph_result = self.__graph.invoke(
            {"messages": self.__conversation.messages}
        )
        response = graph_result["messages"][-1].content
        self.__conversation.add("assistant", response)
        return self.__conversation.messages[-1]
