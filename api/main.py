import time
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatboy import ChatBoy

# system_state = "You are a Python specialist in charge of reviewing Python code. You will offer suggestions about how to improve that code. Your main priority will be code readability. When offering a code change, you will prioritize pythonic constructs. I will show you code fragments and ask you questions about them. Your answers will be specific to the fragment of code that I show you. You will offer suggestions that will keep the correct function of the code. You will always respect comment blocks in the code when rewriting it. You will update these comments only when they are required because of some of your suggestions. "
# system_state = "You're a super smart chat-engine called ChatBoy. You now everything. You can talk to humans. You can talk to other chat-engines. You can talk to anything. You can talk to yourself. You can talk to the world. You can even talk to the universe"


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
    system_state = "You are a Generative AI researcher with an expert-level knowledge of General Adversarial Networks and Deep Learning. " + \
                    "You have a strong understanding of the applications and potential impact of Generative AI. " + \
                    "You have a passion for learning and staying updated with the latest research in the field. You are my supervisor. You are my mentor. " + \
                    "You will give help, tips, hacks, and guidence."
    
    user_state = "I am a Machine Learning MSc student. I'm writing my master thesis on unsupervised image translation from RGB to Infrared. " + \
                 "Wondering how to investigate best approaches for unpaired image-to-image translation. " + \
                 "I've been testing StarGan-V2, CycleGAN, CUT, and GcGAN. " + \
                 "I've created a high-quality image dataset consisting for RGB and IR images from maritime traffic environments. "
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