"""
Test the Multi-Agent System
"""

from src.multi_agent_system import MultiAgentSystem
import json


def test_multi_agent_system():
    """Test the multi-agent system with various tasks."""
    
    print("\n" + "=" * 70)
    print("🧪 Testing Multi-Agent System")
    print("=" * 70)
    
    # Initialize the system
    system = MultiAgentSystem(max_reflection_iterations=3)
    
    # Test cases
    test_cases = [
        {
            'name': 'Research Task',
            'task': "What is the capital of Japan and what is its population?",
            'expected_agent': 'research'
        },
        {
            'name': 'Analysis Task',
            'task': "Write a Python function that calculates the factorial of a number",
            'expected_agent': 'analysis'
        },
        {
            'name': 'Creative Task',
            'task': "Write a short poem about technology",
            'expected_agent': 'creative'
        },
        {
            'name': 'Mixed Task',
            'task': "Research the latest AI trends and write a short summary",
            'expected_agent': 'mixed'
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print("\n" + "=" * 70)
        print(f"📝 Test: {test_case['name']}")
        print(f"Task: {test_case['task']}")
        print("=" * 70)
        
        try:
            result = system.process(test_case['task'])
            
            # Extract the final answer
            final_answer = result.get('final_result', {})
            if final_answer and isinstance(final_answer, dict):
                final_text = final_answer.get('final_result', final_answer.get('result', 'No result'))
            else:
                final_text = str(final_answer) if final_answer else 'No result'
            
            results.append({
                'test': test_case['name'],
                'task': test_case['task'],
                'success': True,
                'result': final_text[:200] + "..." if len(str(final_text)) > 200 else str(final_text),
                'iterations': len(result.get('iterations', [])),
                'expected_agent': test_case['expected_agent']
            })
            
            print(f"\n✅ Test Passed!")
            print(f"Result: {final_text[:200]}...")
            print(f"Iterations: {len(result.get('iterations', []))}")
            
        except Exception as e:
            results.append({
                'test': test_case['name'],
                'task': test_case['task'],
                'success': False,
                'error': str(e)
            })
            print(f"\n❌ Test Failed: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    
    passed = sum(1 for r in results if r.get('success', False))
    total = len(results)
    
    print(f"\n✅ Passed: {passed}/{total}")
    
    print("\nDetails:")
    for r in results:
        status = "✅ PASS" if r.get('success') else "❌ FAIL"
        print(f"  {status} - {r['test']} (Expected: {r.get('expected_agent', 'N/A')})")
        if r.get('success'):
            print(f"        Iterations: {r.get('iterations', 'N/A')}")
        else:
            print(f"        Error: {r.get('error', 'Unknown')}")


if __name__ == "__main__":
    test_multi_agent_system()