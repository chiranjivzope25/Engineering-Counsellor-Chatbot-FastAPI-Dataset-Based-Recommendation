from fastapi import FastAPI
from pydantic import BaseModel
from Counseller_chatbot import handle_query
app=FastAPI()
class Message(BaseModel):
      message:str
@app.get("/")
def home():
    return{"message" : "API is running"}
@app.post("/chat")
def chat(data:Message):
    reply=handle_query(data.message)
    return{"reply":reply}