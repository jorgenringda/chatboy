from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatboy import ChatBoy

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
  message: str

@app.on_event("startup")
def startup() -> None:
    system_state = "You're a super smart chat-engine called ChatBoy. You now everything. You can talk to humans. You can talk to other chat-engines. You can talk to anything. You can talk to yourself. You can talk to the world. You can even talk to the universe"
    app.state.chatboy = ChatBoy(system_state)

@app.on_event("shutdown")
def shutdown() -> None:
    del app.state.chatboy

@app.post("/chat")
async def get_response(message: Message) -> Dict[str, str]:
    return {"response": app.state.chatboy(message.message)}
  
@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Hello World"}