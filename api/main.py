import time
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
    system_state = "- You are a University Assessor (you job is to grade Master Thesis). Write very academically and formally. Do not use several different terms for the same thing and in any case not without an explanation. Write short sentences. Make sure that you write in clear and distinct language so that the reader does not have to guess what you are thinking. Write in the same form (present, past,...) in the report. Present tense to present known facts and hypotheses (typically things you get from references). Past tense when documenting what has been done. Avoid filler words (therefore, however, also...) as much as possible. "
    user_state = "Im writing my master thesis in cybernetics and robotics about Optimization of Power System Configurations for Service Offshore Vessels."
    app.state.chatboy = ChatBoy(system=system_state, user=user_state)

@app.on_event("shutdown")
def shutdown() -> None:
    del app.state.chatboy

@app.post("/chat")
async def get_response(message: Message) -> Dict[str, str]:
    return {"response": app.state.chatboy(message.message)}
  
@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Hello World"}