from prompts.system import get_system_prompt
from dataclass import dataclass
from typing import Any
from utils.text import count_tokens

@dataclass
class MessageItem:
    role: str
    content: str
    token_count: int |None = None
    
    def to_dict(self)->dict[str, Any]:
        result:dict[str,Any] = {"role": self.role}
        if self.content:
            result["content"] = self.content
        return result

class ContextManager:
    def __init__(self)->None:
        self.system_prompt = get_system_prompt()
        self._messages:list[MessageItem] = []
        self._model_name = "nvidia/nron-3-super-120b-a12b:free"
        
    def add_user_message(self, content:str)->None:
        token_count = count_tokens(content, model=self._model_name)
        message = MessageItem(role="user", content=content, token_count=token_count)
        self._messages.append(message)
    
    def add_assistant_message(self, content:str)->None:
        token_count = count_tokens(content, model=self._model_name)
        message = MessageItem(role="assistant", content=content or '', token_count=token_count)
        self._messages.append(message)
        
    def get_messages(self)->lis[dict[str, Any]]:
        messages = []
        if self.system_prompt:
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })
        for item in self._messages:
            messages.append(item.to_dict())
        return messages