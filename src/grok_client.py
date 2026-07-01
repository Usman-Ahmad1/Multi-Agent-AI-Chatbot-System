"""
Groq API Client - Professional Implementation
Handles communication with Groq API with error handling and retry logic.
Note: This uses Groq API (not Grok) - the filename is kept for compatibility.
"""

import os
import time
from typing import Optional, Dict, Any, List
from groq import Groq
from dotenv import load_dotenv


class GroqClient:
    """
    A professional client for interacting with the Groq API.
    Features:
    - Environment variable configuration
    - Automatic retries with exponential backoff
    - Comprehensive error handling
    - Multiple model support
    - Chat completion with history support
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Groq client with API credentials.
        
        Args:
            api_key: Groq API key (optional, reads from .env if not provided)
        """
        # Load environment variables
        load_dotenv()
        
        # Set API key
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found. Set it in .env file or pass to constructor.")
        
        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)
        
        # Available models
        self.models = [
            "llama-3.1-8b-instant",
            "gemma2-9b-it",
            "llama-3.2-3b-preview",
            "llama-3.2-1b-preview",
            "mixtral-8x7b-32768"
        ]
        
        # Configuration
        self.max_retries = 5  # Increased for better rate limit handling
        self.retry_delay = 1
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "llama-3.1-8b-instant",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False
    ):
        """
        Send a chat completion request to the Groq API with rate limit handling.
        """
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=stream
                )
                return response
                
            except Exception as e:
                error_msg = str(e)
                
                # Handle rate limit specifically
                if "429" in error_msg or "rate_limit" in error_msg.lower():
                    wait_time = (2 ** attempt) + 1  # 1s, 2s, 4s, 8s...
                    print(f"⏳ Rate limit hit. Waiting {wait_time}s... (Attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(wait_time)
                    continue
                
                # Handle other errors
                print(f"⚠️ Error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt == self.max_retries - 1:
                    raise Exception(f"Groq API error: {e}")
                time.sleep(self.retry_delay * (2 ** attempt))
        
        raise Exception("Max retries exceeded")
    
    def simple_chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        model: str = "llama-3.1-8b-instant"
    ) -> str:
        """
        Simple method for one-off chat messages.
        
        Args:
            user_message: The user's message
            system_prompt: Optional system prompt to guide the AI
            temperature: Sampling temperature
            model: Model to use
            
        Returns:
            The AI's response as a string
        """
        messages = []
        
        if system_prompt:
            messages.append({
                'role': 'system',
                'content': system_prompt
            })
        
        messages.append({
            'role': 'user',
            'content': user_message
        })
        
        response = self.chat_completion(
            messages=messages,
            temperature=temperature,
            model=model
        )
        
        # Extract the response content
        return response.choices[0].message.content
    
    def test_models(self) -> Dict[str, bool]:
        """
        Test all available models to see which ones work.
        
        Returns:
            Dict with model names as keys and boolean success status
        """
        results = {}
        print("🔍 Testing Groq Models...")
        print("-" * 50)
        
        for model in self.models:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Say 'Hello' in one word"}],
                    max_tokens=10
                )
                print(f"✅ {model} - WORKS")
                results[model] = True
            except Exception as e:
                print(f"❌ {model} - FAILED: {str(e)[:50]}")
                results[model] = False
        
        return results


# ============================================================
# Example Usage (Test the client)
# ============================================================

def main():
    """Test the GroqClient with a sample query."""
    try:
        print("🤖 Groq API Client Test")
        print("=" * 50)
        
        # Create client instance
        client = GroqClient()
        
        print("✅ Client initialized successfully!")
        print(f"   API Key: {client.api_key[:10]}... (hidden)")
        
        # Test available models
        print("\n📋 Testing available models:")
        print("-" * 50)
        client.test_models()
        
        # Send a test message
        print("\n📤 Sending test message...")
        print("-" * 50)
        
        response_text = client.simple_chat(
            user_message="What is the capital of France?",
            system_prompt="You are a helpful assistant. Answer concisely.",
            model="llama-3.1-8b-instant"
        )
        
        print("\n📥 Response:")
        print("-" * 50)
        print(response_text)
        print("-" * 50)
        print("\n✅ Test completed successfully!")
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("Make sure you have set GROQ_API_KEY in your .env file.")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()