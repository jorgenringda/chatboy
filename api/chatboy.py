import os
from typing import Any, Dict, List, Union

import openai
from dotenv import load_dotenv
from openai import ChatCompletion

load_dotenv()
openai.api_key = os.getenv("API_KEY")


class ChatBoy:
    def __init__(self, system: str = "") -> None:
        self.system = system
        self.messages: List[Dict[str, Union[str, Any]]] = []
        if self.system:
            self.messages.append({"role": "system", "content": system})
    
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.process_messages()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def process_messages(self) -> str:
        completion = ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        content = completion.choices[0].message.content
        return self._process_reply(content)    
    
    def _process_reply(self, response: str) -> None:
        return response.strip()