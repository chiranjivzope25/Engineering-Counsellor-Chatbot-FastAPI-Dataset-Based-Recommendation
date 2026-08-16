from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Counseller_chatbot import handle_query

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    message: str


@app.get("/api")
def home():
    return {
        "message": "Chirag Counseller API is running"
    }


@app.post("/api/chat")
def chat(data: Message):
    reply = handle_query(data.message)

    return {
        "reply": reply
    }