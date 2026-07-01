"""
Research Agent - Specializes in finding and summarizing information from the web.
"""

from typing import Dict, Any, Optional
from src.base_agent import BaseAgent
from src.tools import Tools


class ResearchAgent(BaseAgent):
    """
    Research Agent: Expert at finding information, searching the web,
    reading webpages, and summarizing content.
    """
    
    def __init__(self):
        system_prompt = """You are a Research Agent specialized in finding and summarizing information.

Your expertise:
- Web search and information retrieval
- Reading and analyzing webpages
- Summarizing complex topics
- Fact-checking and verification
- Extracting key insights from sources

When given a research task:
1. Identify what information is needed
2. Use web_search to find relevant sources
3. Use read_webpage to extract detailed information
4. Synthesize findings into a clear, concise summary
5. Cite your sources where appropriate

Be thorough but efficient. Focus on accuracy and relevance.
"""
        super().__init__(
            name="ResearchAgent",
            role="Expert at finding and summarizing information from the web",
            system_prompt=system_prompt
        )
        self.tools = Tools()
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a research task.
        
        Args:
            task: The research question or topic
            context: Optional context like previous research results
            
        Returns:
            Dict with research findings
        """
        try:
            # Step 1: Break down the research task
            research_plan = self._plan_research(task)
            
            # Step 2: Execute research steps
            findings = self._conduct_research(task, research_plan)
            
            # Step 3: Synthesize findings
            synthesis = self._synthesize_findings(task, findings)
            
            return {
                'status': 'success',
                'result': synthesis,
                'confidence': 85,
                'sources': findings.get('sources', []),
                'summary': synthesis
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'result': f"Research failed: {str(e)}",
                'confidence': 0
            }
    
    def _plan_research(self, task: str) -> list:
        """Plan the research approach."""
        planning_prompt = f"""
Given this research task: "{task}"

Create a research plan. List 3-5 specific things you need to search for.
Format as a numbered list.
"""
        plan = self._call_llm(planning_prompt, temperature=0.3)
        return plan.split('\n')
    
    def _conduct_research(self, task: str, plan: list) -> Dict[str, Any]:
        """Execute the research plan using tools."""
        findings = {
            'raw_data': [],
            'sources': [],
            'summaries': []
        }
        
        # Use web_search for each search query
        # Note: In a real implementation, we'd parse the plan and search
        # For now, do a single comprehensive search
        
        search_result = self.tools.web_search(task)
        findings['raw_data'].append(search_result)
        
        # Try to read a relevant webpage if search found something
        # This is simplified; in production we'd parse URLs from search results
        if "Wikipedia" in search_result or "Search Results" in search_result:
            # Try to read the first Wikipedia result
            wiki_article = f"https://en.wikipedia.org/wiki/{task.replace(' ', '_')}"
            try:
                webpage_content = self.tools.read_webpage(wiki_article)
                findings['raw_data'].append(webpage_content[:2000])
                findings['sources'].append(wiki_article)
            except:
                pass
        
        return findings
    
    def _synthesize_findings(self, task: str, findings: Dict[str, Any]) -> str:
        """Synthesize all findings into a coherent summary."""
        synthesis_prompt = f"""
You are a Research Agent summarizing findings for the task: "{task}"

Here are the raw findings:
{findings['raw_data']}

Provide a clear, well-structured summary that:
1. Directly answers the research question
2. Includes key facts and insights
3. Is organized with bullet points or sections
4. Cites sources where available
5. Is approximately 200-400 words

Make it professional and informative.
"""
        return self._call_llm(synthesis_prompt, temperature=0.4)