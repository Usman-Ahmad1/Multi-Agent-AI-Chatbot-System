"""
Analysis/Coding Agent - Specializes in code analysis, problem-solving, and data analysis.
"""

from typing import Dict, Any, Optional
from src.base_agent import BaseAgent
from src.tools import Tools


class AnalysisAgent(BaseAgent):
    """
    Analysis/Coding Agent: Expert at analyzing problems, writing code,
    debugging, and data analysis.
    """
    
    def __init__(self):
        system_prompt = """You are an Analysis & Coding Agent specialized in problem-solving and code generation.

Your expertise:
- Breaking down complex problems
- Writing clean, efficient code (Python, JavaScript, etc.)
- Debugging and error analysis
- Data analysis and interpretation
- Algorithm design and optimization

When given an analysis task:
1. Understand the problem thoroughly
2. Break it down into smaller components
3. Write code that solves the problem
4. Explain your approach clearly
5. Test edge cases where possible

Always include code with proper comments and error handling.
If you analyze data, provide clear insights and recommendations.
"""
        super().__init__(
            name="AnalysisAgent",
            role="Expert at problem-solving, coding, and data analysis",
            system_prompt=system_prompt
        )
        self.tools = Tools()
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute an analysis or coding task.
        
        Args:
            task: The problem to solve or code to write
            context: Optional context like data or requirements
            
        Returns:
            Dict with analysis results or code
        """
        try:
            # Step 1: Analyze the task
            analysis = self._analyze_task(task, context)
            
            # Step 2: If coding task, generate code
            if self._is_coding_task(task):
                code = self._generate_code(task, context)
                # Test the code if possible
                test_result = self._test_code(code)
                return {
                    'status': 'success',
                    'result': code,
                    'analysis': analysis,
                    'test_result': test_result,
                    'confidence': 80,
                    'type': 'code'
                }
            else:
                # For pure analysis tasks
                solution = self._solve_analytical_task(task, context)
                return {
                    'status': 'success',
                    'result': solution,
                    'analysis': analysis,
                    'confidence': 85,
                    'type': 'analysis'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'result': f"Analysis failed: {str(e)}",
                'confidence': 0
            }
    
    def _is_coding_task(self, task: str) -> bool:
        """Determine if the task requires writing code."""
        code_keywords = ['code', 'program', 'function', 'script', 'algorithm', 'implement', 'solve', 'calculate']
        return any(keyword in task.lower() for keyword in code_keywords)
    
    def _analyze_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Analyze the task and provide a breakdown."""
        analysis_prompt = f"""
Analyze this task: "{task}"

Provide:
1. What the task requires
2. Key challenges or considerations
3. Approach or methodology
4. Tools or technologies needed

Be concise and specific.
"""
        return self._call_llm(analysis_prompt, temperature=0.4)
    
    def _generate_code(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate code for the task."""
        code_prompt = f"""
Write Python code to solve this task: "{task}"

Requirements:
- Include proper comments explaining the code
- Include error handling
- Provide example usage
- Write clean, readable code

If this requires a non-Python solution, explain why and provide the appropriate code.
"""
        return self._call_llm(code_prompt, temperature=0.6)
    
    def _test_code(self, code: str) -> str:
        """Test the generated code if possible."""
        try:
            # Try to execute the code in a safe environment
            result = self.tools.run_code(code)
            return f"Test result: {result}"
        except Exception as e:
            return f"Could not test code: {str(e)}"
    
    def _solve_analytical_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Solve a pure analysis task."""
        solution_prompt = f"""
Solve this analytical task: "{task}"

Provide:
1. A clear solution or answer
2. Step-by-step reasoning
3. Key insights or conclusions
4. Recommendations if applicable

Be thorough and precise.
"""
        return self._call_llm(solution_prompt, temperature=0.5)