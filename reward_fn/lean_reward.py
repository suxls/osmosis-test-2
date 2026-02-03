from lean_dojo import (
    LeanGitRepo, 
    Theorem, 
    Dojo,
    ProofFinished,
    LeanError,
)
import tempfile
import os
import json

def verify_lean_with_dojo(lean_code_string: str, repo_url: str, theorem_name: str) -> int:
    """
    Verify Lean code using Lean Dojo's Dojo environment.
    Requires an actual Lean repository with the theorem.
    
    Args:
        lean_code_string: The Lean code (for reference)
        repo_url: GitHub URL of Lean repository containing the code
        theorem_name: Name of the theorem to verify
    
    Returns:
        1 if theorem type-checks and can be accessed, 0 otherwise
    """
    
    try:
        # Point to mathlib4 with v4.11.0
        repo = LeanGitRepo(
            url=repo_url,
            commit=None  # Uses HEAD, update to specific commit if needed
        )
        
        # Specify the file and theorem to verify
        # You'd need to know the file path and theorem name
        theorem = Theorem(repo, "lean_files/Four.lean", "intersection_subset_left")
        
        # Try to open the Dojo environment (this checks if theorem exists)
        with Dojo(theorem) as (dojo, init_state):
            # If we can open the Dojo without errors, the theorem is valid
            # init_state contains the initial proof state
            if init_state is not None:
                return 1
            else:
                return 0
                
    except Exception as e:
        print(f"Dojo verification failed: {str(e)}")
        return 0


# Example usage:
if __name__ == "__main__":
    # Example 1: Simple Lean code
    simple_code = """
    theorem test : 2 + 2 = 4 := by
        decide
    """
    
    result = verify_lean_simple(simple_code)
    print(f"Verification result: {result}")
    
    # Example 2: Code with syntax error
    invalid_code = """
import Mathlib open scoped ENNReal NNReal Nat open MeasureTheory Real Set Filter Topology theorem poissonPMFRealSum_extracted (r : ℝ≥0) : HasSum (fun n => ProbabilityTheory.poissonPMFReal r n) 1 := sorry
    """
    result = verify_lean_simple(invalid_code)
    print(f"Invalid code verification: {result}")
    
  
