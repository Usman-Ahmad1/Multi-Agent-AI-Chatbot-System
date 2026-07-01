"""
Multi-Agent System - Orchestrates the entire multi-agent workflow.
Includes speed optimizations, self-reflection, and human-in-the-loop capabilities.
"""

from typing import Dict, Any, Optional
from src.supervisor_agent import SupervisorAgent
from src.verification_agent import VerificationAgent


class MultiAgentSystem:
    """
    Multi-Agent System: Orchestrates the supervisor and specialist agents.
    Includes self-reflection, human-in-the-loop, and speed optimization.
    """
    
    def __init__(self, max_reflection_iterations: int = 3, skip_verification: bool = False):
        """
        Initialize the multi-agent system.
        
        Args:
            max_reflection_iterations: Maximum number of self-reflection cycles
            skip_verification: If True, skip verification for faster responses
        """
        self.supervisor = SupervisorAgent()
        self.verification_agent = VerificationAgent()
        self.max_reflection_iterations = max_reflection_iterations
        self.skip_verification = skip_verification
        
    def _is_simple_task(self, task: str) -> bool:
        """
        Check if a task is simple enough to skip verification.
        This speeds up response time for basic queries.
        
        Args:
            task: The task string to evaluate
            
        Returns:
            True if the task is simple and can skip verification
        """
        # Keywords that indicate a simple task
        simple_keywords = [
            'hello', 'hi', 'hey', 'test', 'simple', 'basic',
            'what is', 'weather', 'calculate', 'math', 'add',
            'subtract', 'multiply', 'divide', 'capital', 'population'
        ]
        
        # Simple tasks are short and contain simple keywords
        task_lower = task.lower()
        is_short = len(task) < 50
        has_simple_keyword = any(keyword in task_lower for keyword in simple_keywords)
        
        return is_short and has_simple_keyword
    
    def process(self, task: str, human_feedback: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a task using the multi-agent system with self-reflection.
        
        Args:
            task: The task to process
            human_feedback: Optional human feedback for the self-reflection loop
            
        Returns:
            Dict with the final result and processing history
        """
        history = {
            'task': task,
            'iterations': [],
            'final_result': None,
            'human_feedback': human_feedback,
            'mode': 'fast' if self.skip_verification else 'thorough'
        }
        
        # Initial processing
        print(f"\n🧠 Multi-Agent System Processing: {task}")
        print("=" * 70)
        
        for iteration in range(self.max_reflection_iterations):
            print(f"\n🔄 Iteration {iteration + 1}/{self.max_reflection_iterations}")
            print("-" * 40)
            
            # Step 1: Route and execute the task
            if iteration == 0:
                # Check if this is a simple task that can skip verification
                if self.skip_verification or self._is_simple_task(task):
                    print("⚡ Fast mode: Skipping verification for simple task...")
                    result = self.supervisor.route_task(task, {'human_feedback': human_feedback})
                    result['verification'] = {'status': 'skipped', 'reason': 'Simple task or fast mode'}
                else:
                    result = self.supervisor.route_task(task, {'human_feedback': human_feedback})
            else:
                # Add previous feedback to context
                context = {
                    'human_feedback': human_feedback,
                    'previous_iterations': history['iterations'],
                    'previous_result': history['iterations'][-1] if history['iterations'] else None
                }
                result = self.supervisor.route_task(task, context)
            
            # Step 2: Self-reflection (skip if fast mode or simple task)
            if self.skip_verification or self._is_simple_task(task) or iteration == 0:
                # For fast mode, create a simple reflection without API call
                if self.skip_verification or self._is_simple_task(task):
                    reflection = {
                        'status': 'skipped',
                        'score': 85,
                        'issues': 'Verification skipped for speed',
                        'improvements': 'Use balanced or thorough mode for deeper analysis',
                        'analysis': 'Fast mode used for quick response',
                        'is_acceptable': True
                    }
                else:
                    reflection = self._self_reflect(task, result, iteration)
            else:
                reflection = self._self_reflect(task, result, iteration)
            
            result['reflection'] = reflection
            
            # Store in history
            history['iterations'].append({
                'iteration': iteration + 1,
                'result': result,
                'reflection': reflection,
                'mode': 'fast' if self.skip_verification else 'normal'
            })
            
            # Step 3: Check if we should continue
            if self._is_satisfactory(result, reflection):
                print(f"\n✅ Task completed satisfactorily in {iteration + 1} iterations!")
                history['final_result'] = result
                break
            
            # Step 4: If not satisfactory and not the last iteration
            if iteration < self.max_reflection_iterations - 1:
                # Prepare for next iteration with feedback
                improvement_suggestions = self._get_improvement_suggestions(result, reflection)
                human_feedback = f"Previous result needs improvement. Suggestions: {improvement_suggestions}"
                print(f"\n📝 Refining with feedback...")
            else:
                # Last iteration - use the best we have
                print(f"\n⚠️ Reached maximum iterations. Using best available result.")
                history['final_result'] = result
        
        # If no final result set, use the last result
        if history['final_result'] is None and history['iterations']:
            history['final_result'] = history['iterations'][-1]['result']
        
        return history
    
    def _self_reflect(self, task: str, result: Dict[str, Any], iteration: int) -> Dict[str, Any]:
        """
        Perform self-reflection on the result.
        """
        print(f"\n💭 Self-Reflection (Iteration {iteration + 1})...")
        
        # Use the verification agent to critique the result
        final_result = result.get('final_result', '')
        if not final_result:
            return {
                'status': 'no_result',
                'score': 0,
                'assessment': 'No result to reflect on.',
                'is_acceptable': False
            }
        
        try:
            reflection_result = self.verification_agent.execute(
                final_result, 
                {'task': task, 'context': 'This is a self-reflection assessment.'}
            )
            
            # Extract key reflections
            if reflection_result.get('status') == 'success':
                reflection_data = reflection_result.get('result', {})
                return {
                    'status': 'completed',
                    'score': reflection_data.get('score', 0),
                    'issues': reflection_data.get('issues', ''),
                    'improvements': reflection_data.get('improvements', ''),
                    'analysis': reflection_data.get('analysis', ''),
                    'is_acceptable': reflection_data.get('is_acceptable', False)
                }
            else:
                return {
                    'status': 'error',
                    'score': 0,
                    'assessment': 'Could not perform self-reflection.',
                    'is_acceptable': False
                }
        except Exception as e:
            return {
                'status': 'error',
                'score': 0,
                'assessment': f'Self-reflection error: {str(e)}',
                'is_acceptable': False
            }
    
    def _is_satisfactory(self, result: Dict[str, Any], reflection: Dict[str, Any]) -> bool:
        """
        Determine if the result is satisfactory based on reflection.
        """
        # If reflection was skipped (fast mode), always accept
        if reflection.get('status') == 'skipped':
            return True
        
        if reflection.get('status') == 'completed':
            score = reflection.get('score', 0)
            return score >= 70
        
        return False
    
    def _get_improvement_suggestions(self, result: Dict[str, Any], reflection: Dict[str, Any]) -> str:
        """
        Extract improvement suggestions for the next iteration.
        """
        if reflection.get('status') == 'completed':
            improvements = reflection.get('improvements', '')
            if improvements and len(improvements) > 10:
                return improvements
        
        # Default improvement suggestions
        return "Please improve the response by being more thorough, accurate, and providing more specific details."
    
    def process_with_speed_mode(self, task: str, mode: str = 'balanced') -> Dict[str, Any]:
        """
        Process a task with a specific speed mode.
        
        Args:
            task: The task to process
            mode: One of 'fast', 'balanced', or 'thorough'
            
        Returns:
            Dict with the final result and processing history
        """
        mode_configs = {
            'fast': {'iterations': 1, 'skip_verification': True},
            'balanced': {'iterations': 2, 'skip_verification': False},
            'thorough': {'iterations': 3, 'skip_verification': False}
        }
        
        config = mode_configs.get(mode, mode_configs['balanced'])
        self.max_reflection_iterations = config['iterations']
        self.skip_verification = config['skip_verification']
        
        return self.process(task)


# Quick test function
def test_multi_agent_system():
    """Quick test of the multi-agent system."""
    print("\n🧪 Testing Multi-Agent System")
    print("=" * 50)
    
    # Test with different modes
    system = MultiAgentSystem()
    
    # Test query
    test_task = "What is the capital of France?"
    
    print(f"\n📝 Test: {test_task}")
    
    # Run with balanced mode
    result = system.process_with_speed_mode(test_task, mode='balanced')
    
    # Show result
    final_result = result.get('final_result', {})
    if isinstance(final_result, dict):
        text = final_result.get('final_result', final_result.get('result', 'No result'))
    else:
        text = str(final_result) if final_result else 'No result'
    
    print(f"\n✅ Result: {text[:200]}...")
    print(f"📊 Iterations: {len(result.get('iterations', []))}")
    print(f"⚡ Mode: {result.get('mode', 'unknown')}")


if __name__ == "__main__":
    test_multi_agent_system()