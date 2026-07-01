"""
Base Agent Class - All specialist agents inherit from this.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from src.grok_client import GroqClient


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the multi-agent system.
    Each agent has a specific role and expertise.
    """
    
    def __init__(self, name: str, role: str, system_prompt: str):
        """
        Initialize the base agent.
        
        Args:
            name: Agent's name (e.g., "ResearchAgent")
            role: Agent's role description (e.g., "Expert at finding information")
            system_prompt: The system prompt that defines this agent's behavior
        """
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.client = GroqClient()
        
    @abstractmethod
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the agent's primary function.
        
        Args:
            task: The task to perform
            context: Additional context (previous results, etc.)
            
        Returns:
            Dict containing:
                - 'status': 'success' or 'error'
                - 'result': The agent's output
                - 'confidence': Score 0-100 (optional)
        """
        pass
    
    def _call_llm(
        self, 
        user_message: str, 
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Internal method to call the LLM with the agent's system prompt.
        """
        messages = [
            {'role': 'system', 'content': self.system_prompt},
            {'role': 'user', 'content': user_message}
        ]
        
        try:
            response = self.client.chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def __repr__(self) -> str:
        return f"{self.name} (Role: {self.role})"