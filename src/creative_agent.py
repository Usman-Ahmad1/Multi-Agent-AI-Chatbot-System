"""
Creative Agent - Specializes in creative writing, brainstorming, and content generation.
"""

from typing import Dict, Any, Optional
from src.base_agent import BaseAgent


class CreativeAgent(BaseAgent):
    """
    Creative Agent: Expert at creative writing, brainstorming ideas,
    generating content, and creative problem-solving.
    """
    
    def __init__(self):
        system_prompt = """You are a Creative Agent specialized in creative thinking and content generation.

Your expertise:
- Creative writing and storytelling
- Brainstorming and ideation
- Content creation (articles, emails, social media posts)
- Creative problem-solving
- Generating engaging and original ideas

When given a creative task:
1. Think outside the box
2. Generate multiple ideas or options
3. Be original and engaging
4. Consider the target audience
5. Provide creative and actionable content

Be imaginative but also practical. Your output should be both creative and useful.
"""
        super().__init__(
            name="CreativeAgent",
            role="Expert at creative writing, brainstorming, and content generation",
            system_prompt=system_prompt
        )
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a creative task.
        
        Args:
            task: The creative task (write, brainstorm, generate content)
            context: Optional context like audience or constraints
            
        Returns:
            Dict with creative output
        """
        try:
            # Step 1: Understand the creative brief
            brief = self._understand_brief(task, context)
            
            # Step 2: Generate creative output
            output = self._generate_creative_content(task, brief)
            
            # Step 3: Refine and polish
            refined = self._refine_content(output, task)
            
            return {
                'status': 'success',
                'result': refined,
                'brief': brief,
                'confidence': 80,
                'type': 'creative'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'result': f"Creative task failed: {str(e)}",
                'confidence': 0
            }
    
    def _understand_brief(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Understand the creative brief."""
        brief_prompt = f"""
Task: "{task}"

If context is provided: {context}

Break down this creative task:
1. What type of content is needed?
2. Who is the target audience?
3. What is the tone or style?
4. Any constraints or requirements?
5. What should be the key message or goal?

Provide a clear creative brief.
"""
        return self._call_llm(brief_prompt, temperature=0.4)
    
    def _generate_creative_content(self, task: str, brief: str) -> str:
        """Generate creative content."""
        creative_prompt = f"""
Creative Task: "{task}"

Creative Brief:
{brief}

Generate creative content that:
- Is original and engaging
- Matches the tone and style required
- Meets the needs of the target audience
- Is well-structured and polished

Be creative and imaginative while staying focused on the task.
"""
        return self._call_llm(creative_prompt, temperature=0.8)  # Higher temperature for creativity
    
    def _refine_content(self, content: str, task: str) -> str:
        """Refine and polish the creative content."""
        refine_prompt = f"""
Original creative content for task: "{task}"

Content:
{content}

Refine this content by:
1. Improving clarity and flow
2. Enhancing engagement and impact
3. Checking for any gaps or missing elements
4. Polishing the language and style

Provide the refined version.
"""
        return self._call_llm(refine_prompt, temperature=0.5)