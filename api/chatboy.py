import json
import logging
import os
from typing import Any, Dict, List, Union

import openai
from dotenv import load_dotenv
from openai import ChatCompletion
from openai.error import APIError, InvalidRequestError, RateLimitError

load_dotenv()
openai.api_key = os.getenv("API_KEY")

def setup_logger(name: str, log_file: str, level=logging.INFO):
    DEFAULT_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(DEFAULT_FORMATTER)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

os.makedirs("logs", exist_ok=True)
logchat = setup_logger('chat', 'logs/chat.log')
logerror = setup_logger('error', 'logs/error.log')

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
        logchat.info(f'Message: {message}')
        
        try:
            response = self.process_messages()
        except InvalidRequestError as emcle:
            logerror.exception('An exception occurred while processing messages: %s', emcle)
            is_successfull = False
            self._reset_messages() # Full message history => so reset
            response = "INFO \n " + json.dumps(emcle.exception) + "\n" + "Deleting all messages ..."
        except APIError as ae:
            logerror.exception('An exception occurred while processing messages: %s', ae)
            is_successfull = False
            response = json.dumps(ae.error)
        except RateLimitError as rle:
            logerror.exception('An exception occurred while processing messages: %s', rle)
            is_successfull = False
            response = json.dumps(rle.error)
            
        logchat.info(f'Response: {response}')
        
        if is_successfull:
            self.messages.append({"role": "assistant", "content": response})
        return response
    
    def process_messages(self) -> str:
        completion = ChatCompletion.create(model=self.model, messages=self.messages)
        return self._process_reply(completion)
    
    def _process_reply(self, completion: dict) -> None:
        response = completion.choices[0].message.content
        return response.strip()