
"""
Redis-backed Short-Term Memory
Same interface as ShortTermMemory, but backed by Redis instead of RAM deque.
Survives across processes, supports auto-expiration.
"""

import json
import redis
from typing import List, Dict
from config.settings import get_settings


class RedisShortTermMemory:
    """
    Stores recent conversation messages in Redis (as a list per user).
    Same method names as ShortTermMemory for drop-in compatibility.
    """
    
    def __init__(self, max_messages: int = 10):
        settings = get_settings()
        self.max_messages = max_messages
        self.ttl_seconds = settings.redis_ttl_seconds
        
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True  # so we get strings back, not bytes
        )
    
    def _key(self, user_id: str) -> str:
        """Build the Redis key for a given user's conversation buffer"""
        return f"chat:history:{user_id}"
    
    def add_message(self, user_id: str, role: str, content: str):
        """
        Add a message to the user's buffer in Redis
        
        Args:
            user_id: Identifies whose conversation this belongs to
            role: "user" or "assistant"
            content: The message text
        """
        key = self._key(user_id)
        message = json.dumps({"role": role, "content": content})
        
        # Push to the right end of the list (like deque.append)
        self.client.rpush(key, message)
        
        # Trim to keep only the last N messages (like deque's maxlen)
        self.client.ltrim(key, -self.max_messages, -1)
        
        # Reset expiration timer every time there's activity
        self.client.expire(key, self.ttl_seconds)
    
    def get_messages(self, user_id: str) -> List[Dict[str, str]]:
        """Get all messages currently in the user's buffer, oldest first"""
        key = self._key(user_id)
        raw_messages = self.client.lrange(key, 0, -1)
        return [json.loads(msg) for msg in raw_messages]
    
    def get_recent_text(self, user_id: str) -> str:
        """Get buffer as a readable text block (useful for prompts)"""
        messages = self.get_messages(user_id)
        lines = []
        for msg in messages:
            lines.append(f"{msg['role'].capitalize()}: {msg['content']}")
        return "\n".join(lines)
    
    def clear(self, user_id: str):
        """Clear the buffer for a specific user"""
        key = self._key(user_id)
        self.client.delete(key)


# Quick test
if __name__ == "__main__":
    memory = RedisShortTermMemory(max_messages=3)
    
    user_id = "test_user"
    memory.clear(user_id)  # Start fresh
    
    memory.add_message(user_id, "user", "Hello!")
    memory.add_message(user_id, "assistant", "Hi there!")
    memory.add_message(user_id, "user", "What's the weather?")
    memory.add_message(user_id, "assistant", "I don't have weather access.")  # Pushes out "Hello!"
    
    print("✅ Buffer contents:")
    for msg in memory.get_messages(user_id):
        print(f"  {msg}")
    
    print("\n✅ As text:")
    print(memory.get_recent_text(user_id))
    
    # Check TTL was set
    key = memory._key(user_id)
    ttl = memory.client.ttl(key)
    print(f"\n✅ TTL remaining: {ttl} seconds")