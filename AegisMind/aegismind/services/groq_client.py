"""
Groq API client wrapper
Treats LLM as stateless reasoning engine
"""

from groq import Groq 
from typing import List,Dict,Optional
from aegismind.config.settings import get_settings


class GroqClient:
    """Wrapper for Groq API calls """
    def __init__(self):
        self.settings=get_settings()
        self.client =Groq(api_key=self.settings.groq_api_key)
        self.model=self.settings.groq_model
        
        
    def generate(
        self,
        messages:List[Dict[str,str]],
        temperature:float =0.7,
        max_tokens:int=1000,
        system_prompt:Optional[str]=None     
    ) -> str :
        """
        Generate  a response using Groq 
        Args:
            messages:List of chat messages [{"role":"user","content":"..."}]
            temperature:Randomness(0-1)
            max_tokens: Max response length
            system_prompt:Optional system instruction 
        
        Returns:
            Generated text    
        """    
        
        # Prepare messages:
        formatted_messages=[]
        
        if system_prompt:
            formatted_messages.append({
                "role": "system",
                "content": system_prompt
            })
        formatted_messages.extend(messages)   
        
        try:
            response =self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens    
            ) 
            return response.choices[0].message.content 
        except Exception as e:
            raise RuntimeError(f"Groq API error: {str(e)}")
        
    def generate_structured(
        self,
        messages:List[Dict[str,str]],
        system_prompt:str,
        temperature:float =0.3   
        )-> str :
        """
        Generate structured output (for planning/routing)
        Uses lower temperature for consistency
        
        """
        return self.generate(
            messages=messages,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=500   
        )
        
        
        



        
        
        
        
        
