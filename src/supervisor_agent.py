"""
Supervisor Agent - Routes tasks to the appropriate specialist agents.
"""

from typing import Dict, Any, Optional, List
from src.base_agent import BaseAgent
from src.research_agent import ResearchAgent
from src.analysis_agent import AnalysisAgent
from src.creative_agent import CreativeAgent
from src.verification_agent import VerificationAgent


class SupervisorAgent:
    """
    Supervisor Agent: Analyzes tasks and routes them to the right specialist agent.
    Coordinates the multi-agent workflow.
    """
    
    def __init__(self):
        """Initialize the supervisor with all specialist agents."""
        self.agents = {
            'research': ResearchAgent(),
            'analysis': AnalysisAgent(),
            'creative': CreativeAgent(),
            'verification': VerificationAgent()
        }
        self.client = self.agents['research'].client  # Use any agent's client
        
    def route_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Route a task to the appropriate specialist agent.
        
        Args:
            task: The task to perform
            context: Optional context
            
        Returns:
            Dict with routing decision and result
        """
        # Step 1: Classify the task
        classification = self._classify_task(task)
        
        # Step 2: Determine which agent(s) to use
        agent_assignment = self._assign_agents(classification, task)
        
        # Step 3: Execute with the assigned agent(s)
        results = self._execute_with_agents(task, agent_assignment, context)
        
        # Step 4: Optionally verify the result
        if len(agent_assignment) > 0 and not self._is_simple_task(task):
            verification_result = self._verify_result(task, results)
            results['verification'] = verification_result
        
        return results
    
    def _classify_task(self, task: str) -> str:
        """
        Classify the task type.
        Returns: 'research', 'analysis', 'creative', 'mixed', or 'unknown'
        """
        task_lower = task.lower()
        
        # Keywords for classification
        research_keywords = ['search', 'find', 'research', 'what', 'who', 'when', 'where', 'learn', 'information', 'source']
        analysis_keywords = ['code', 'program', 'function', 'analyze', 'calculate', 'solve', 'debug', 'data', 'algorithm']
        creative_keywords = ['write', 'create', 'generate', 'brainstorm', 'design', 'story', 'poem', 'article', 'idea']
        
        scores = {
            'research': sum(1 for word in research_keywords if word in task_lower),
            'analysis': sum(1 for word in analysis_keywords if word in task_lower),
            'creative': sum(1 for word in creative_keywords if word in task_lower)
        }
        
        # Determine primary category
        max_score = max(scores.values())
        if max_score == 0:
            return 'research'  # Default to research
        
        primary = max(scores, key=scores.get)
        
        # Check if it's mixed
        categories = [cat for cat, score in scores.items() if score >= 1]
        if len(categories) > 1 and sum(scores.values()) > 2:
            return 'mixed'
        
        return primary
    
    def _assign_agents(self, classification: str, task: str) -> List[str]:
        """
        Assign one or more agents to handle the task.
        """
        if classification == 'research':
            return ['research']
        elif classification == 'analysis':
            return ['analysis']
        elif classification == 'creative':
            return ['creative']
        elif classification == 'mixed':
            # For mixed tasks, use multiple agents in sequence
            task_lower = task.lower()
            agents = []
            
            if any(word in task_lower for word in ['search', 'find', 'what', 'who', 'learn']):
                agents.append('research')
            if any(word in task_lower for word in ['code', 'analyze', 'calculate', 'solve']):
                agents.append('analysis')
            if any(word in task_lower for word in ['write', 'create', 'generate']):
                agents.append('creative')
            
            return agents if agents else ['research']
        else:
            return ['research']
    
    def _execute_with_agents(self, task: str, agent_names: List[str], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the task with the assigned agents.
        """
        results = {
            'task': task,
            'agents_used': agent_names,
            'results': {},
            'final_result': ''
        }
        
        combined_context = context or {}
        
        for agent_name in agent_names:
            agent = self.agents.get(agent_name)
            if not agent:
                continue
            
            # Add previous results to context
            if results['results']:
                combined_context['previous_results'] = results['results']
            
            # Execute the agent
            result = agent.execute(task, combined_context)
            results['results'][agent_name] = result
            
            # If it's a code task and we have a successful result
            if agent_name == 'analysis' and result.get('type') == 'code' and result.get('status') == 'success':
                # Try to run the code and add test results
                pass
            
            # If it's a research task, use the summary as final result
            if agent_name == 'research' and result.get('status') == 'success':
                results['final_result'] = result.get('result', '')
        
        # If no final result set, use the last result
        if not results['final_result'] and results['results']:
            last_result = list(results['results'].values())[-1]
            results['final_result'] = last_result.get('result', '')
        
        return results
    
    def _verify_result(self, task: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify the final result using the Verification Agent.
        """
        final_result = results.get('final_result', '')
        if not final_result:
            return {'status': 'skipped', 'reason': 'No result to verify'}
        
        verification_agent = self.agents['verification']
        verification_result = verification_agent.execute(final_result, {'task': task})
        
        return verification_result
    
    def _is_simple_task(self, task: str) -> bool:
        """Check if a task is simple enough to skip verification."""
        simple_keywords = ['simple', 'basic', 'hello', 'test']
        return any(word in task.lower() for word in simple_keywords) and len(task) < 30