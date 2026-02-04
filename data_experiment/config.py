import pandas as pd
import re

SYSTEM_PROMPT = """
You are a Lean4 auto-formalization engine.

## Task
Given a statement of a math problem,translate it into formal language Lean4 code.
Do not write any proof step for this theorem or try to solve this problem , you should focus on the translation ONLY.
Simply use "sorry" as a place holder of the detailed proof if necessary. 
The resulting lean statement should start with "theorem" and end with ":= sorry".

Example: 
User: "Solve for $x$ in the given inequality: $x^2-2x-24<0$"
Solution: theorem example_1 (x : ℝ) : x^2 - 2*x - 24 < 0 ↔ x ∈ Set.Ioo (-4) 6   :=  by sorry
"""


# Cache the workbook in-memory so we don't re-read it per row.
_WORKBOOK_DF: pd.DataFrame | None = None

_HERALD_STMT_DF: pd.DataFrame | None = None

def _strip_header(statement: str) -> str:
    ## strip everything before the first occurance of "theorem"
    return re.sub(r'^.*theorem', 'theorem', statement)

def _get_workbook_df() -> pd.DataFrame:
    global _WORKBOOK_DF
    if _WORKBOOK_DF is None:
        _WORKBOOK_DF = pd.read_parquet("workbook.parquet")
    return _WORKBOOK_DF

def _get_herald_stmt_df() -> pd.DataFrame:
    global _HERALD_STMT_DF
    if _HERALD_STMT_DF is None:
        _HERALD_STMT_DF = pd.read_parquet("herald_stmt.parquet")
    return _HERALD_STMT_DF

def generate_lean_example_workbook() -> dict:
    '''
    Generate a single Lean4 auto-formalization training example.
    '''
    df = _get_workbook_df()
    row = df.sample(n=1).iloc[0]

    nl_statement = row["natural_language_statement"]
    formal_statement = row["formal_statement"]

    return {
        # Ensure plain Python strings (not pandas Series) for Arrow/JSON serialization.
        "user_prompt": str(nl_statement),
        "system_prompt": SYSTEM_PROMPT.strip(),
        "ground_truth": str(formal_statement),
    }

def generate_lean_example_herald_stmt() -> dict:
    '''
    Generate a single Lean4 auto-formalization training example.
    '''
    df = _get_herald_stmt_df()
    row = df.sample(n=1).iloc[0]

    nl_statement = row["informal_statement"]
    formal_statement = row["formal_statement"]

    return {
        "user_prompt": str(nl_statement),
        "system_prompt": SYSTEM_PROMPT.strip(),
        "ground_truth": _strip_header(str(formal_statement)),
    }


