"""
Optimized Multi-Agent System with Speed Control
"""

from src.multi_agent_system import MultiAgentSystem


class OptimizedMultiAgentSystem(MultiAgentSystem):
    """Optimized version with speed controls."""
    
    def __init__(self, mode='balanced'):
        if mode == 'fast':
            max_iterations = 1
        elif mode == 'thorough':
            max_iterations = 3
        else:
            max_iterations = 2
        
        super().__init__(max_iterations=max_iterations)
        self.mode = mode
    
    def process(self, task: str, human_feedback: str = None):
        # Skip verification for fast mode
        if self.mode == 'fast':
            # Directly use supervisor without verification
            result = self.supervisor.route_task(task, {'human_feedback': human_feedback})
            return {
                'task': task,
                'iterations': [{'iteration': 1, 'result': result}],
                'final_result': result,
                'mode': 'fast'
            }
        
        # Use normal processing for other modes
        return super().process(task, human_feedback)