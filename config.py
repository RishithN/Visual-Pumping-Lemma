"""
Configuration and constants for the Visual Pumping Lemma Demonstrator
"""

# Predefined languages with their properties
PREDEFINED_LANGUAGES = {
    "regular": {
        "L1": {
            "description": "aⁿbᵐ | n, m ≥ 0",
            "pattern": "a^n b^m",
            "type": "regular"
        },
        "L2": {
            "description": "(ab)ⁿ | n ≥ 0",
            "pattern": "(ab)*",
            "type": "regular"
        },
        "L3": {
            "description": "Strings with even number of a's",
            "pattern": "(b*ab*ab*)*",
            "type": "regular"
        }
    },
    "non_regular": {
        "L4": {
            "description": "aⁿbⁿ | n ≥ 0",
            "pattern": "a^n b^n",
            "type": "non_regular"
        },
        "L5": {
            "description": "aⁿbⁿcⁿ | n ≥ 0", 
            "pattern": "a^n b^n c^n",
            "type": "non_regular"
        },
        "L6": {
            "description": "ww | w ∈ {a,b}*",
            "pattern": "ww",
            "type": "non_regular"
        }
    },
    "context_free": {
        "L7": {
            "description": "aⁿbⁿ | n ≥ 0 (CFL)",
            "pattern": "a^n b^n",
            "type": "context_free"
        },
        "L8": {
            "description": "wwᴿ | w ∈ {a,b}*",
            "pattern": "w w_reverse",
            "type": "context_free"
        },
        "L9": {
            "description": "Bal parentheses",
            "pattern": "balanced_parentheses",
            "type": "context_free"
        }
    }
}

# Colors for visualization
COLORS = {
    'x': '#1f77b4',      # blue
    'y': '#ff7f0e',      # orange
    'z': '#2ca02c',      # green
    'u': '#d62728',      # red
    'v': '#9467bd',      # purple
    'w': '#8c564b',      # brown
    'x_cfl': '#e377c2',  # pink
    'y_cfl': '#7f7f7f',  # gray
    'pumped': '#ffff00', # yellow for pumped parts
    'background': '#f0f0f0'
}

# Animation settings
ANIMATION_CONFIG = {
    'duration': 1000,
    'transition': 500,
    'max_iterations': 5
}

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