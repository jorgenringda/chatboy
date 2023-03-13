import json
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, List, Union

import openai
from dotenv import load_dotenv
from openai import ChatCompletion
from openai.error import APIError, InvalidRequestError

load_dotenv()
openai.api_key = os.getenv("API_KEY")
logging.basicConfig(filename='logs/chat.log', level=logging.INFO, format='%(asctime)s: %(message)s')

class MaximumContentLengthExceeded(InvalidRequestError):
    def __init__(self, max_length: int = 4096, message: str = "Input text length exceeds maximum allowed length."):
        self.max_length = max_length
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Maximum allowed length: {self.max_length}."

class ChatBoy:
    def __init__(self, system: str = "", user: str = "") -> None:
        self.system = system
        self.user = user
        self.model = "gpt-3.5-turbo"
        self._reset_messages()
            
    def _reset_messages(self) -> None:
        self.messages: List[Dict[str, Union[str, Any]]] = []
        if self.system:
            self.messages.append({"role": "system", "content": self.system})
        if self.user:
            self.messages.append({"role": "user", "content": self.user})
        
    
    def __call__(self, message):
        is_successfull, response = True, ""
        
        self.messages.append({"role": "user", "content": message})
        
        logging.info(f'Message: {message}')
        try:
            response = self.process_messages()
        except InvalidRequestError as emcle:
            is_successfull = False
            self._reset_messages()
            response = "INFO \n " + json.dumps(emcle.error) + "\n" + "Deleting all messages ..."
        except APIError as ae:
            is_successfull = False
            response = json.dumps(ae.error)
            
        logging.info(f'Response: {response}')
        
        if is_successfull:
            self.messages.append({"role": "assistant", "content": response})
        return response
    
    def process_messages(self) -> str:
        completion = ChatCompletion.create(model=self.model, messages=self.messages)
        return self._process_reply(completion)
    
    def _process_reply(self, completion: dict) -> None:
        response = completion.choices[0].message.content
        return response.strip()
    
    
# Refactor and apply best practices.


