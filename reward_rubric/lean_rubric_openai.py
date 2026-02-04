from osmosis_ai import (
    evaluate_rubric,
    osmosis_rubric,
)
import os

# make life easier by hardcoding the rubric, score range and model info
RUBRIC = """
You are a Lean4 statement similarity scorer.

You are given two strings:
(1) a predicted Lean4 statement
(2) a ground-truth Lean4 statement

Your task is to output a single numeric reward in [0, 1].

Rules:
- Output 0 if the predicted string is empty or clearly not a Lean4 theorem statement.
- Output 1 if the two statements are textually identical up to whitespace, formatting,
  and variable renaming.
- Otherwise output a number strictly between 0 and 1 based on surface-level similarity
  of structure and symbols.

Constraints:
- Do NOT check Lean4 parsing, elaboration, or kernel validity.
- Do NOT reason step-by-step.
- Do NOT explain your answer.

Only respond with a single number between 0 and 1.
"""
SCORE_MIN = 0.0
SCORE_MAX = 1.0
PROVIDER = "openai"
MODEL = "gpt-5-mini"
API_KEY = os.getenv("OPENAI_API_KEY")

@osmosis_rubric
def compute_rubric_score_openai(
    solution_str: str,
    ground_truth: str,
    extra_info: dict,
    **kwargs
) -> float:
    """
    Delegate rubric scoring to a hosted model while keeping @osmosis_rubric validation.
    """
    model_info = {"provider": PROVIDER, "model": MODEL, "api_key": API_KEY}
    prompt_metadata = extra_info.get("metadata")

    result = evaluate_rubric(
        rubric=RUBRIC,
        solution_str=solution_str,
        model_info=model_info,
        ground_truth=ground_truth,
        metadata=prompt_metadata,
        score_min=SCORE_MIN,
        score_max=SCORE_MAX,
        return_details=False,
    )

    return float(result)
