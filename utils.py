"""
Utility functions for the Pumping Lemma Demonstrator
"""
import re
import random
from typing import List, Tuple, Dict, Any

def generate_test_strings(language_pattern: str, min_length: int = 1, max_length: int = 10) -> List[str]:
    """
    Generate test strings based on language pattern
    """
    strings = []
    
    if language_pattern == "a^n b^n":
        for n in range(min_length, max_length + 1):
            strings.append('a' * n + 'b' * n)
    
    elif language_pattern == "a^n b^m":
        for n in range(min_length, max_length + 1):
            for m in range(min_length, max_length + 1):
                strings.append('a' * n + 'b' * m)
    
    elif language_pattern == "a*b*":
        for n in range(min_length, max_length + 1):
            for m in range(min_length, max_length + 1):
                strings.append('a' * n + 'b' * m)
    
    elif language_pattern == "(ab)*":
        for n in range(min_length, max_length + 1):
            strings.append('ab' * n)
    
    elif language_pattern == "a^n b^n c^n":
        for n in range(min_length, min(4, max_length) + 1):  # Limit for performance
            strings.append('a' * n + 'b' * n + 'c' * n)
    
    elif language_pattern == "ww":
        samples = ['aa', 'abab', 'aaaabb', 'abcabc']
        strings = [s for s in samples if min_length <= len(s) <= max_length]
    
    elif language_pattern == "w w_reverse":
        samples = ['aa', 'abba', 'abcba', 'aabbaa']
        strings = [s for s in samples if min_length <= len(s) <= max_length]
    
    elif language_pattern == "(b*ab*ab*)*":
        # Strings with even number of a's
        samples = ['', 'aa', 'baab', 'abab', 'baba', 'bb', 'aabb', 'bbaa', 'abba']
        strings = [s for s in samples if min_length <= len(s) <= max_length]
    
    # If no strings generated, create some simple ones
    if not strings:
        strings = ['a', 'aa', 'aaa', 'b', 'bb', 'bbb', 'ab', 'aab', 'abb'][:max_length]
    
    return strings

def is_string_in_language(s: str, language_pattern: str) -> bool:
    """
    Check if a string belongs to the given language
    """
    if language_pattern == "a^n b^n":
        a_count = len(re.findall('a', s))
        b_count = len(re.findall('b', s))
        return s.startswith('a') and s.endswith('b') and a_count == b_count and 'ba' not in s
    
    elif language_pattern == "a^n b^m":
        return bool(re.fullmatch(r'a*b*', s))
    
    elif language_pattern == "a*b*":
        return bool(re.fullmatch(r'a*b*', s))
    
    elif language_pattern == "(ab)*":
        return bool(re.fullmatch(r'(ab)*', s))
    
    elif language_pattern == "a^n b^n c^n":
        a_match = re.match(r'^(a+)b+c+$', s)
        if a_match:
            n = len(a_match.group(1))
            return s == 'a' * n + 'b' * n + 'c' * n
        return False
    
    elif language_pattern == "ww":
        if len(s) % 2 == 0:
            half = len(s) // 2
            return s[:half] == s[half:]
        return False
    
    elif language_pattern == "w w_reverse":
        if len(s) % 2 == 0:
            half = len(s) // 2
            return s[:half] == s[half:][::-1]
        return False
    
    elif language_pattern == "(b*ab*ab*)*":
        # Strings with even number of a's
        a_count = s.count('a')
        return a_count % 2 == 0 and all(c in 'ab' for c in s)
    
    return False

def calculate_pumping_length(language_type: str, language_pattern: str) -> int:
    """
    Estimate pumping length based on language properties
    """
    if language_type == "regular":
        if language_pattern == "a^n b^n":
            return 3  # For aⁿbⁿ, p should be at least 2, but we use 3 for demonstration
        elif language_pattern in ["a*b*", "a^n b^m"]:
            return 1  # Any string length works
        else:
            return 2
    
    elif language_type == "context_free":
        if language_pattern == "a^n b^n c^n":
            return 5  # For aⁿbⁿcⁿ, p should account for all three symbols
        else:
            return 3
    
    return 2

def validate_language_input(language_input: str) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validate user language input and extract components
    """
    language_input = language_input.strip()
    
    # Check for common patterns
    patterns = {
        r'a\^?n\s*b\^?n': "a^n b^n",
        r'a\^?n\s*b\^?m': "a^n b^m", 
        r'a\^*\s*b\^*': "a*b*",
        r'\(ab\)\^*': "(ab)*",
        r'a\^?n\s*b\^?n\s*c\^?n': "a^n b^n c^n",
        r'ww': "ww",
        r'w\s*w_r(everse)?': "w w_reverse",
        r'\(b\*ab\*ab\*\)\*': "(b*ab*ab*)*"
    }
    
    for pattern, standardized in patterns.items():
        if re.search(pattern, language_input, re.IGNORECASE):
            # Determine type based on pattern
            if standardized in ["a^n b^n", "a^n b^n c^n", "ww"]:
                lang_type = "non_regular"
            elif standardized in ["w w_reverse"]:
                lang_type = "context_free"
            else:
                lang_type = "regular"
                
            return True, standardized, {
                "description": language_input,
                "pattern": standardized,
                "type": lang_type
            }
    
    return False, "Invalid pattern", {}