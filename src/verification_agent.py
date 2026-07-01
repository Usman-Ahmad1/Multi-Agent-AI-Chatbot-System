"""
Verification/Critique Agent - Specializes in reviewing, critiquing, and improving outputs.
"""

from typing import Dict, Any, Optional
from src.base_agent import BaseAgent


class VerificationAgent(BaseAgent):
    """
    Verification/Critique Agent: Expert at reviewing outputs, identifying issues,
    suggesting improvements, and ensuring quality.
    """
    
    def __init__(self):
        system_prompt = """You are a Verification & Critique Agent specialized in quality assurance and improvement.

Your expertise:
- Critical analysis and review
- Identifying errors, inconsistencies, and gaps
- Suggesting improvements and enhancements
- Quality assurance and validation
- Providing constructive feedback

When given content to verify:
1. Analyze it thoroughly
2. Identify strengths and weaknesses
3. Point out any errors or issues
4. Suggest specific improvements
5. Provide a quality score (0-100)
6. Recommend whether it's ready or needs revision

Be thorough, honest, and constructive. Your goal is to improve quality.
"""
        super().__init__(
            name="VerificationAgent",
            role="Expert at reviewing, critiquing, and improving outputs",
            system_prompt=system_prompt
        )
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a verification/critique task.
        
        Args:
            task: The content to review and critique
            context: Optional context like expectations or criteria
            
        Returns:
            Dict with critique and improvement suggestions
        """
        try:
            # Step 1: Analyze the content
            analysis = self._analyze_content(task, context)
            
            # Step 2: Identify issues and strengths
            issues = self._identify_issues(task, analysis)
            
            # Step 3: Suggest improvements
            improvements = self._suggest_improvements(task, issues)
            
            # Step 4: Provide quality score
            score = self._score_quality(task, issues)
            
            return {
                'status': 'success',
                'result': {
                    'analysis': analysis,
                    'issues': issues,
                    'improvements': improvements,
                    'score': score,
                    'is_acceptable': score >= 70
                },
                'confidence': 85
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'result': f"Verification failed: {str(e)}",
                'confidence': 0
            }
    
    def _analyze_content(self, content: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Analyze the content thoroughly."""
        analysis_prompt = f"""
Analyze this content:

{content}

Provide a comprehensive analysis covering:
1. Main strengths
2. Weaknesses or gaps
3. Clarity and structure
4. Accuracy and completeness
5. Relevance to the task

Be thorough and specific.
"""
        return self._call_llm(analysis_prompt, temperature=0.3)
    
    def _identify_issues(self, content: str, analysis: str) -> str:
        """Identify specific issues."""
        issues_prompt = f"""
Content: {content}

Analysis: {analysis}

List specific issues found:
1. Errors (factual, logical, grammatical)
2. Gaps or missing information
3. Clarity problems
4. Inconsistencies
5. Other issues

Be specific and actionable.
"""
        return self._call_llm(issues_prompt, temperature=0.3)
    
    def _suggest_improvements(self, content: str, issues: str) -> str:
        """Suggest specific improvements."""
        improvements_prompt = f"""
Original content: {content}

Issues found: {issues}

Provide specific, actionable suggestions to improve this content:
1. What to change
2. What to add
3. What to remove
4. How to restructure
5. Any other recommendations

Make each suggestion clear and practical.
"""
        return self._call_llm(improvements_prompt, temperature=0.5)
    
    def _score_quality(self, content: str, issues: str) -> int:
        """Score the quality of the content."""
        score_prompt = f"""
Content: {content}

Issues: {issues}

Based on the analysis and issues identified, provide a quality score from 0-100 where:
- 90-100: Excellent, ready for use
- 70-89: Good, minor improvements needed
- 50-69: Needs work, significant issues
- 0-49: Needs major revisions

Provide only the number (no explanation).
"""
        try:
            score_response = self._call_llm(score_prompt, temperature=0.1, max_tokens=10)
            # Extract number from response
            import re
            score_match = re.search(r'\d+', score_response)
            score = int(score_match.group()) if score_match else 50
            return max(0, min(100, score))  # Clamp between 0-100
        except:
            return 50  # Default score if parsing fails