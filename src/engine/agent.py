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
        self.__graph = create_react_agent(
            ChatGroq(model=Environment.GROQ_MODEL),
            tools=[self.search_products]
        )

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

    @tool
    def search_products(
        self,
        query: str
    ) -> str:
        """
        Search for products based on the provided query.
        Args:
            query (str): The search query to find relevant products.
        Returns:
            str: A string representation of the search results.
        """
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
