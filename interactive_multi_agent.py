"""
Interactive Multi-Agent System - Chat with all agents!
"""

from src.multi_agent_system import MultiAgentSystem

def interactive_chat():
    """Interactive chat with the multi-agent system."""
    
    system = MultiAgentSystem(max_reflection_iterations=3)
    
    print("\n" + "=" * 70)
    print("🤖 Multi-Agent System - Interactive Mode")
    print("=" * 70)
    print("Commands:")
    print("  /exit  - Quit")
    print("  /help  - Show this help")
    print("  /agents - Show available agents")
    print("=" * 70)
    
    while True:
        try:
            user_input = input("\n🧑 You: ").strip()
            
            if user_input.lower() in ['/exit', '/quit']:
                print("👋 Goodbye!")
                break
                
            if user_input.lower() == '/help':
                print("\nCommands:")
                print("  /exit  - Quit")
                print("  /help  - Show this help")
                print("  /agents - Show available agents")
                continue
                
            if user_input.lower() == '/agents':
                print("\nAvailable Agents:")
                print("  🔍 Research Agent - Finds and summarizes information")
                print("  💻 Analysis Agent - Writes code and analyzes problems")
                print("  🎨 Creative Agent - Writes poems, stories, and creative content")
                print("  ✅ Verification Agent - Critiques and improves outputs")
                continue
                
            if not user_input:
                continue
            
            print("\n" + "=" * 70)
            print("🧠 Processing...")
            print("=" * 70)
            
            # Process the query
            result = system.process(user_input)
            
            # Extract the final answer
            final_result = result.get('final_result', {})
            if final_result and isinstance(final_result, dict):
                final_text = final_result.get('final_result', final_result.get('result', 'No result'))
            else:
                final_text = str(final_result) if final_result else 'No result'
            
            print("\n" + "=" * 70)
            print("🤖 Final Answer:")
            print("=" * 70)
            print(final_text)
            print("=" * 70)
            print(f"📊 Iterations: {len(result.get('iterations', []))}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    interactive_chat()