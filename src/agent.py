"""
ReAct Agent with Tools
"""

import sys
import os
import re
from typing import Dict, Any

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import from src
from src.grok_client import GroqClient
from src.tools import Tools


class ReActAgent:
    """ReAct (Reason + Act) Agent that uses tools to solve problems."""
    
    def __init__(self, max_iterations: int = 5):
        self.client = GroqClient()
        self.tools = Tools()
        self.max_iterations = max_iterations
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the ReAct agent."""
        tool_descriptions = []
        for name in self.tools.get_tool_names():
            desc = self.tools.get_tool_description(name)
            tool_descriptions.append(f"  - {name}: {desc}")
        
        tools_section = "\n".join(tool_descriptions)
        
        return f"""
You are a ReAct (Reason + Act) agent that can use tools to solve problems.

## Available Tools:
{tools_section}

## How to respond:
1. **Reason**: Think about what you need to do.
2. **Act**: Use one tool at a time.
3. **Observe**: Wait for the tool result.
4. **Repeat**: Continue until you have enough information.

## Format for using tools:
To use a tool, respond with:
TOOL: tool_name
INPUT: input_string

For example:
TOOL: web_search
INPUT: latest AI news 2026

Or:
TOOL: calculate
INPUT: 2 + 2 * 10

## Important:
- Use tools when you need information or computation.
- If you have enough information, respond directly to the user.
- Always verify information when possible.
- Be concise but thorough in your reasoning.
"""
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the agent's response to extract tool usage or final answer."""
        tool_match = re.search(r'TOOL:\s*(\w+)\s*INPUT:\s*(.+?)(?=\n\n|\nTOOL:|$)', 
                               response, re.DOTALL | re.IGNORECASE)
        
        if tool_match:
            return {
                'type': 'tool_use',
                'tool': tool_match.group(1).strip().lower(),
                'input': tool_match.group(2).strip()
            }
        
        return {'type': 'final_answer', 'content': response.strip()}
    
    def _execute_tool(self, tool_name: str, tool_input: str) -> str:
        """Execute a tool and return the result."""
        tool_func = self.tools.get_tool(tool_name)
        if not tool_func:
            return f"❌ Unknown tool: {tool_name}"
        
        try:
            result = tool_func(tool_input)
            return f"Tool Result: {result}"
        except Exception as e:
            return f"❌ Tool execution error: {str(e)}"
    
    def process(self, user_query: str) -> str:
        """Process a user query using the ReAct loop."""
        print("\n" + "="*70)
        print(f"🧠 Agent Processing: {user_query}")
        print("="*70)
        
        conversation = [
            {'role': 'system', 'content': self.system_prompt},
            {'role': 'user', 'content': user_query}
        ]
        
        for iteration in range(self.max_iterations):
            print(f"\n🔄 Step {iteration + 1}/{self.max_iterations}")
            print("-" * 40)
            
            try:
                response = self.client.chat_completion(
                    messages=conversation,
                    model="llama-3.1-8b-instant",
                    temperature=0.3,
                    max_tokens=500
                )
                
                agent_response = response.choices[0].message.content
                print(f"💭 Agent:\n{agent_response}")
                
                parsed = self._parse_response(agent_response)
                
                if parsed['type'] == 'final_answer':
                    print("\n" + "="*70)
                    print("✅ Final Answer:")
                    print(parsed['content'])
                    print("="*70)
                    return parsed['content']
                
                elif parsed['type'] == 'tool_use':
                    tool_name = parsed['tool']
                    tool_input = parsed['input']
                    
                    print(f"\n🔧 Using Tool: {tool_name}")
                    print(f"📥 Input: {tool_input}")
                    
                    tool_result = self._execute_tool(tool_name, tool_input)
                    print(f"📤 Result:\n{tool_result}")
                    
                    conversation.append({'role': 'assistant', 'content': agent_response})
                    conversation.append({'role': 'user', 'content': f"Tool Result: {tool_result}\n\nContinue with the next step or provide final answer."})
                
            except Exception as e:
                print(f"\n❌ Error in step {iteration + 1}: {e}")
                return f"I encountered an error: {e}"
        
        print("\n⚠️ Maximum iterations reached.")
        return "I was unable to complete the task within the maximum steps."
    
    def interactive_chat(self):
        """Interactive chat mode for the agent."""
        print("\n" + "="*70)
        print("🤖 ReAct Agent Interactive Mode")
        print("="*70)
        print("Commands: /exit, /help")
        print("="*70)
        
        while True:
            try:
                user_input = input("\n🧑 You: ").strip()
                if user_input.lower() in ['/exit', '/quit']:
                    print("👋 Goodbye!")
                    break
                if user_input.lower() == '/help':
                    print("\nCommands: /exit, /help")
                    continue
                if not user_input:
                    continue
                
                self.process(user_input)
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Test the ReAct agent."""
    agent = ReActAgent(max_iterations=5)
    
    print("\n" + "="*70)
    print("🚀 ReAct Agent with Tools")
    print("="*70)
    
    test_query = "Search for the capital of France and also calculate 100 divided by 4"
    print(f"\n📝 Test Query: {test_query}")
    print("="*70)
    
    response = agent.process(test_query)
    print(f"\n📄 Final Response: {response}")


if __name__ == "__main__":
    main()