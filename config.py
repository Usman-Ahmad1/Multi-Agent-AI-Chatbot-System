"""
Configuration for Multi-Agent System
"""

class Config:
    # Speed vs Quality Settings
    FAST_MODE = {
        'max_iterations': 1,
        'skip_verification': True,
        'temperature': 0.3,
        'model': 'llama-3.1-8b-instant',
        'timeout': 10
    }
    
    BALANCED_MODE = {
        'max_iterations': 2,
        'skip_verification': False,
        'temperature': 0.7,
        'model': 'llama-3.1-8b-instant',
        'timeout': 20
    }
    
    THOROUGH_MODE = {
        'max_iterations': 3,
        'skip_verification': False,
        'temperature': 0.9,
        'model': 'llama-3.1-8b-instant',
        'timeout': 30
    }
    
    @classmethod
    def get_mode(cls, mode='balanced'):
        """Get configuration for a specific mode."""
        modes = {
            'fast': cls.FAST_MODE,
            'balanced': cls.BALANCED_MODE,
            'thorough': cls.THOROUGH_MODE
        }
        return modes.get(mode, cls.BALANCED_MODE)