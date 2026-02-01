"""
Language parser for analyzing and validating formal languages
"""
import re
from typing import List, Tuple, Dict, Any, Set
from utils import is_string_in_language

class LanguageParser:
    def __init__(self):
        self.supported_patterns = {
            "a^n b^n", "a^n b^m", "a*b*", "(ab)*", 
            "a^n b^n c^n", "ww", "w w_reverse", "(b*ab*ab*)*"
        }
    
    def parse_language_definition(self, definition: str) -> Dict[str, Any]:
        """
        Parse a language definition and extract its properties
        """
        definition = definition.strip().lower()
        
        # Map user input to standardized patterns
        pattern_map = {
            r'a\^{0,1}n\s*b\^{0,1}n': "a^n b^n",
            r'a\^{0,1}n\s*b\^{0,1}m': "a^n b^m",
            r'a\*b\*': "a*b*",
            r'\(ab\)\*': "(ab)*",
            r'a\^{0,1}n\s*b\^{0,1}n\s*c\^{0,1}n': "a^n b^n c^n",
            r'ww': "ww",
            r'w\s*w_r(everse)?': "w w_reverse",
            r'\(b\*ab\*ab\*\)\*': "(b*ab*ab*)*"
        }
        
        standardized_pattern = None
        for pattern, std_pattern in pattern_map.items():
            if re.fullmatch(pattern, definition.replace(' ', '')):
                standardized_pattern = std_pattern
                break
        
        if not standardized_pattern:
            # Try to handle custom regex
            try:
                re.compile(definition)
                standardized_pattern = definition
            except:
                return {"valid": False, "error": "Unsupported language pattern"}
        
        # Determine language type
        if standardized_pattern in ["a^n b^n", "a^n b^n c^n", "ww"]:
            lang_type = "non_regular"
        elif standardized_pattern in ["w w_reverse"]:
            lang_type = "context_free"
        else:
            lang_type = "regular"
        
        return {
            "valid": True,
            "pattern": standardized_pattern,
            "type": lang_type,
            "description": definition
        }
    
    def generate_sample_strings(self, pattern: str, count: int = 5) -> List[str]:
        """
        Generate sample strings that belong to the language
        """
        samples = []
        
        if pattern == "a^n b^n":
            for n in range(1, count + 1):
                samples.append('a' * n + 'b' * n)
        
        elif pattern == "a^n b^m":
            for i in range(1, count + 1):
                samples.append('a' * i + 'b' * i)
                if i < count:
                    samples.append('a' * i + 'b' * (i + 1))
        
        elif pattern == "a*b*":
            samples = ['', 'a', 'b', 'aa', 'bb', 'aaa', 'bbb', 'aab', 'abb']
        
        elif pattern == "(ab)*":
            for n in range(count + 1):
                samples.append('ab' * n)
        
        elif pattern == "a^n b^n c^n":
            for n in range(1, min(4, count) + 1):
                samples.append('a' * n + 'b' * n + 'c' * n)
        
        elif pattern == "ww":
            samples = ['aa', 'abab', 'aaaabb', 'abcabc']
        
        elif pattern == "w w_reverse":
            samples = ['aa', 'abba', 'abcba', 'aabbaa']
        
        elif pattern == "(b*ab*ab*)*":
            # Strings with even number of a's
            samples = ['', 'aa', 'baab', 'abab', 'baba', 'bb', 'aabb', 'bbaa', 'abba']
        
        # Ensure we don't return more than count samples
        samples = samples[:count]
        
        # If no samples generated, create some simple ones
        if not samples:
            samples = ['a', 'aa', 'b', 'bb', 'ab', 'aab', 'abb'][:count]
        
        return samples
    
    def analyze_language_complexity(self, pattern: str) -> Dict[str, Any]:
        """
        Analyze the computational complexity of the language
        """
        complexity_info = {
            "a^n b^n": {
                "level": "Context-Free",
                "automaton": "PDA required",
                "grammar": "S → aSb | ε"
            },
            "a^n b^m": {
                "level": "Regular", 
                "automaton": "DFA sufficient",
                "grammar": "S → aS | bB | ε, B → bB | ε"
            },
            "a*b*": {
                "level": "Regular",
                "automaton": "Simple DFA",
                "grammar": "S → aS | bB | ε, B → bB | ε"
            },
            "(ab)*": {
                "level": "Regular",
                "automaton": "DFA with 2 states",
                "grammar": "S → abS | ε"
            },
            "a^n b^n c^n": {
                "level": "Context-Sensitive",
                "automaton": "LBA required",
                "grammar": "Non-context-free"
            },
            "ww": {
                "level": "Context-Sensitive", 
                "automaton": "LBA required",
                "grammar": "Non-context-free"
            },
            "w w_reverse": {
                "level": "Context-Free",
                "automaton": "PDA sufficient", 
                "grammar": "S → aSa | bSb | ε"
            },
            "(b*ab*ab*)*": {
                "level": "Regular",
                "automaton": "DFA with 2 states (based on parity of a's)",
                "grammar": "S → bS | aT, T → bT | aS"
            }
        }
        
        return complexity_info.get(pattern, {})