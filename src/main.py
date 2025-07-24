from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from engine.agent import Agent
from engine.db import DB
from populate_db import populate

db = DB()
populate(db)


class QueryInput(BaseModel):
    user_id: str
    query: str


app = FastAPI()
users_dict: dict[str, Agent] = {}


@app.post("/query")
def query(message: QueryInput):
    agent: Optional[Agent] = users_dict.get(message.user_id, None)
    if agent is None:
        agent = Agent(db)
        users_dict[message.user_id] = agent
    return agent.send_message(message.query)


@app.get("/all_products")
def all_products():
    return db.all()
