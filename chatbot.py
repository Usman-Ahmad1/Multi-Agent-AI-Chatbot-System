"""
Interactive Chatbot CLI using Groq API
"""

import sys
from src.grok_client import GroqClient


def chat_loop():
    """
    Interactive chatbot loop with conversation history.
    """
    print("🤖 Groq Chatbot")
    print("=" * 60)
    print("Type 'exit' to quit, 'clear' to clear history")
    print("-" * 60)
    
    try:
        # Initialize the client
        client = GroqClient()
        print("✅ Chatbot ready!\n")
        
        # Conversation history
        conversation = []
        
        # System prompt
        system_prompt = "You are a helpful, friendly AI assistant. Answer questions concisely and helpfully."
        
        while True:
            # Get user input
            user_input = input("\n🧑 You: ").strip()
            
            # Handle commands
            if user_input.lower() == 'exit':
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'clear':
                conversation = []
                print("🗑️ Conversation history cleared!")
                continue
            
            if not user_input:
                continue
            
            # Add user message to conversation
            conversation.append({
                'role': 'user',
                'content': user_input
            })
            
            # Build messages with system prompt
            messages = [{'role': 'system', 'content': system_prompt}] + conversation
            
            try:
                # Get response from Groq
                print("🤔 Thinking...", end="", flush=True)
                
                response = client.chat_completion(
                    messages=messages,
                    model="llama-3.1-8b-instant",
                    temperature=0.7,
                    max_tokens=500
                )
                
                # Extract response text
                ai_message = response.choices[0].message.content
                
                # Print response
                print("\r🤖 AI: " + ai_message)
                
                # Add AI response to conversation
                conversation.append({
                    'role': 'assistant',
                    'content': ai_message
                })
                
            except Exception as e:
                print(f"\r❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("Make sure GROQ_API_KEY is set in .env file.")


def main():
    """Main entry point."""
    try:
        chat_loop()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()