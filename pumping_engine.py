"""
Core pumping lemma logic for regular and context-free languages
"""
import random
from typing import List, Tuple, Dict, Any, Optional
from utils import is_string_in_language

class PumpingEngine:
    def __init__(self):
        self.results = {}
    
    def apply_regular_pumping_lemma(self, language_pattern: str, input_string: str, p: int) -> Dict[str, Any]:
        """
        Apply pumping lemma for regular languages
        """
        result = {
            "string": input_string,
            "pumping_length": p,
            "decomposition": {},
            "iterations": [],
            "lemma_holds": False,
            "language_type": "Unknown"
        }
        
        n = len(input_string)
        
        if n < p:
            result["error"] = f"String length ({n}) is less than pumping length ({p})"
            return result
        
        # Try to find a decomposition that satisfies the lemma
        decompositions = self._generate_regular_decompositions(input_string, p)
        
        for decomp in decompositions:
            x, y, z = decomp["x"], decomp["y"], decomp["z"]
            
            # Test pumping iterations
            iterations = []
            valid_for_all_i = True
            
            for i in [0, 1, 2, 3, 5]:  # Test multiple iterations
                pumped_string = x + (y * i) + z
                is_in_language = is_string_in_language(pumped_string, language_pattern)
                
                iterations.append({
                    "i": i,
                    "pumped_string": pumped_string,
                    "in_language": is_in_language,
                    "parts": {
                        "x": x,
                        "y": y,
                        "z": z,
                        "y_repetitions": i
                    }
                })
                
                if not is_in_language:
                    valid_for_all_i = False
            
            # If we found a decomposition that works for all i, lemma holds
            if valid_for_all_i:
                result["decomposition"] = decomp
                result["iterations"] = iterations
                result["lemma_holds"] = True
                result["language_type"] = "Possibly Regular"
                break
            else:
                # Store the first counterexample
                if not result["iterations"]:
                    result["decomposition"] = decomp
                    result["iterations"] = iterations
                    result["lemma_holds"] = False
                    result["language_type"] = "Not Regular"
        
        return result
    
    def apply_cfl_pumping_lemma(self, language_pattern: str, input_string: str, p: int) -> Dict[str, Any]:
        """
        Apply pumping lemma for context-free languages
        """
        result = {
            "string": input_string,
            "pumping_length": p,
            "decomposition": {},
            "iterations": [],
            "lemma_holds": False,
            "language_type": "Unknown"
        }
        
        n = len(input_string)
        
        if n < p:
            result["error"] = f"String length ({n}) is less than pumping length ({p})"
            return result
        
        # Generate CFL decompositions
        decompositions = self._generate_cfl_decompositions(input_string, p)
        
        for decomp in decompositions:
            u, v, w, x, y = decomp["u"], decomp["v"], decomp["w"], decomp["x"], decomp["y"]
            
            # Test pumping iterations
            iterations = []
            valid_for_all_i = True
            
            for i in [0, 1, 2, 3]:
                pumped_string = u + (v * i) + w + (x * i) + y
                is_in_language = is_string_in_language(pumped_string, language_pattern)
                
                iterations.append({
                    "i": i,
                    "pumped_string": pumped_string,
                    "in_language": is_in_language,
                    "parts": {
                        "u": u,
                        "v": v,
                        "w": w,
                        "x": x,
                        "y": y,
                        "v_repetitions": i,
                        "x_repetitions": i
                    }
                })
                
                if not is_in_language:
                    valid_for_all_i = False
            
            if valid_for_all_i:
                result["decomposition"] = decomp
                result["iterations"] = iterations
                result["lemma_holds"] = True
                result["language_type"] = "Possibly Context-Free"
                break
            else:
                if not result["iterations"]:
                    result["decomposition"] = decomp
                    result["iterations"] = iterations
                    result["lemma_holds"] = False
                    result["language_type"] = "Not Context-Free"
        
        return result
    
    def _generate_regular_decompositions(self, s: str, p: int) -> List[Dict[str, str]]:
        """
        Generate all possible xyz decompositions for regular pumping lemma
        """
        decompositions = []
        n = len(s)
        
        # Try different splits according to pumping lemma conditions
        for split_point in range(1, min(p, n) + 1):
            for y_length in range(1, split_point + 1):
                x = s[:split_point - y_length]
                y = s[split_point - y_length:split_point]
                z = s[split_point:]
                
                if len(y) > 0 and len(x + y) <= p:
                    decompositions.append({
                        "x": x,
                        "y": y,
                        "z": z,
                        "split_info": f"|xy| = {len(x + y)}, |y| = {len(y)}"
                    })
        
        return decompositions
    
    def _generate_cfl_decompositions(self, s: str, p: int) -> List[Dict[str, str]]:
        """
        Generate uvwxy decompositions for CFL pumping lemma
        """
        decompositions = []
        n = len(s)
        
        # Try different splits that satisfy |vwx| <= p and |vx| > 0
        for vwx_start in range(n):
            for vwx_end in range(vwx_start + 1, min(vwx_start + p, n) + 1):
                vwx = s[vwx_start:vwx_end]
                
                # Split vwx into v, w, x
                for v_end in range(1, len(vwx)):
                    for x_start in range(v_end, len(vwx)):
                        v = vwx[:v_end]
                        w = vwx[v_end:x_start]
                        x = vwx[x_start:]
                        
                        if len(v + x) > 0:  # |vx| > 0
                            u = s[:vwx_start]
                            y = s[vwx_end:]
                            
                            decompositions.append({
                                "u": u,
                                "v": v,
                                "w": w,
                                "x": x,
                                "y": y,
                                "split_info": f"|vwx| = {len(vwx)}, |vx| = {len(v + x)}"
                            })
        
        return decompositions[:10]  # Limit to first 10 for performance
    
    def analyze_language_properties(self, language_pattern: str, test_strings: List[str]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of language properties
        """
        analysis = {
            "pattern": language_pattern,
            "test_results": [],
            "properties": {}
        }
        
        for test_string in test_strings:
            is_in_lang = is_string_in_language(test_string, language_pattern)
            analysis["test_results"].append({
                "string": test_string,
                "in_language": is_in_lang,
                "length": len(test_string)
            })
        
        # Determine language characteristics
        strings_in_lang = [r for r in analysis["test_results"] if r["in_language"]]
        
        if strings_in_lang:
            analysis["properties"] = {
                "can_be_empty": any(s["string"] == "" for s in strings_in_lang),
                "min_length": min(s["length"] for s in strings_in_lang),
                "max_length_tested": max(s["length"] for s in strings_in_lang),
                "sample_count": len(strings_in_lang)
            }
        
        return analysis