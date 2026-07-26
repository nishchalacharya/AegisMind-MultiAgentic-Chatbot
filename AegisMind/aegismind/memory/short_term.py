# memory for short-term memory management for last 10 messages as config on settings.py 
"""
Short-Term Memory - Recent conversation buffer
Lives only in RAM for the duration of the session
"""

from typing import List,Dict 
from collections import deque 


class ShortTermMemory: 
    """
    Stores recent conversations messages in a rolling buffer (deque) for short-term memory management. 
    Oldest messages are dropped once max size is reached. This allows for efficient memory usage while retaining recent context.
    """

    def __init__(self,max_messages:int = 10):
        self.max_messages =  max_messages 
        self.buffer : deque =  deque(maxlen=max_messages)  # Rolling buffer for recent messages

    def add_message(self,role:str,content:str):
        """
        Add  a message to the buffer 

        Args: 
            role: "user" or "assistant" 
            content: The message text content 
        """

        self.buffer.append({"role":role,"content":content})

    
    def get_messages(self) -> List[Dict[str,str]]:
        """
        Get all messages currently in buffer ,oldest first 
        """

        return list(self.buffer)
    
    
    def get_recent_text(self)-> str: 
        """Get buffer as a readable text block(useful for prompts)"""
        lines = []
        for msg in self.buffer:
            lines.append(f"{msg['role'].capitalize()}: {msg['content']}")
            
        return "\n".join(lines)
        
    
    def clear(self):
        """Clear the buffer"""
        self.buffer.clear()



# Quick test 

if __name__ == "__main__":
    memory =  ShortTermMemory(max_messages=3)

    memory.add_message("user", "Hello!")
    memory.add_message("assistant", "Hi there!")
    memory.add_message("user", "What's the weather?")
    memory.add_message("assistant", "I don't have weather access.")  # This pushes out "Hello!"
    
    print(" Buffer contents:")
    for msg in memory.get_messages():
        print(f"  {msg}")
    
    print("\n As text:")
    print(memory.get_recent_text())


        









