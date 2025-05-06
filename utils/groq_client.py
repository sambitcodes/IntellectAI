"""
Groq API client integration for the AI Storytelling App.
"""
import os
from typing import Dict, List, Optional
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage

# Available models
AVAILABLE_MODELS = [
    "llama3-70b-8192",
    "llama-3.3-70b-versatile",
    "gemma2-9b-it",
    "deepseek-r1-distill-llama-70b",
    "qwen-qwq-32b"
]

class GroqGenerator:
    """Wrapper for Groq API integration."""
    
    def __init__(self, model_name: str = "llama3-70b-8192", temperature: float = 0.7):
        """
        Initialize the Groq client.
        
        Args:
            model_name: The name of the Groq model to use
            temperature: Controls randomness in generation (0.0-1.0)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.llm = ChatGroq(
            model_name=model_name,
            temperature=temperature,
        )
        
    def generate_content(self, prompt_template: str, **kwargs) -> str:
        """
        Generate content using the Groq model.
        
        Args:
            prompt_template: The prompt template to use
            **kwargs: Variables to be formatted into the prompt template
            
        Returns:
            The generated text content
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke(kwargs)
    
    def chat_with_history(self, messages: List[Dict], system_prompt: Optional[str] = None) -> str:
        """
        Continue a conversation with message history.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_prompt: Optional system prompt to guide the model
            
        Returns:
            The model's response
        """
        langchain_messages = []
        
        # Add system prompt if provided
        if system_prompt:
            langchain_messages.append({"role": "system", "content": system_prompt})
        
        # Convert messages to LangChain format
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
        
        # Special handling for DeepSeek model to extract thinking
        if self.model_name == "deepseek-r1-distill-llama-70b":
            # Add instruction to show thinking
            if langchain_messages[-1].type == "human":
                langchain_messages[-1] = HumanMessage(
                    content=f"{langchain_messages[-1].content}\n\nThink step by step before responding. Begin with '<thinking>' and end your thinking with '</thinking>' before giving your final answer."
                )
        
        response = self.llm.invoke(langchain_messages)
        return response.content
    
    def update_model(self, model_name: str, temperature: float = None):
        """
        Update the model being used.
        
        Args:
            model_name: The name of the new model to use
            temperature: Optional new temperature value
        """
        self.model_name = model_name
        if temperature is not None:
            self.temperature = temperature
        
        self.llm = ChatGroq(
            model_name=model_name,
            temperature=self.temperature,
        )
        
    @staticmethod
    def parse_deepseek_thinking(response: str) -> tuple:
        """
        Parse thinking and answer parts from DeepSeek model responses.
        
        Args:
            response: The full response from the model
            
        Returns:
            A tuple of (thinking, answer) parts
        """
        thinking = ""
        answer = response
        
        if "<thinking>" in response and "</thinking>" in response:
            parts = response.split("</thinking>", 1)
            if len(parts) == 2:
                thinking = parts[0].split("<thinking>", 1)[1].strip()
                answer = parts[1].strip()
        
        return thinking, answer