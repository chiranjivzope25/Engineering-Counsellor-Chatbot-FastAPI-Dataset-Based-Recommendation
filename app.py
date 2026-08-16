from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Counseller_chatbot import handle_query

# 1. Initialize FastAPI FIRST
app = FastAPI()

# 2. Add CORS Middleware AFTER initializing app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/chat")
def chat(data: Message):
    reply = handle_query(data.message)
    return {"reply": reply}