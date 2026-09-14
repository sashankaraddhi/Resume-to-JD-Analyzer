import json
import re
from typing import Any


def build_analysis_prompt(
    resume_text: str,
    jd_text: str,
) -> str:

    return f"""
Analyze the following resume against the following job description.

========================
RESUME
========================

{resume_text}

========================
JOB DESCRIPTION
========================

{jd_text}

========================
REQUIRED ANALYSIS
========================

1. Calculate an overall match percentage.
2. Identify important JD requirements missing from the resume.
3. Provide concrete improvement suggestions.

Return ONLY valid JSON using this structure:

{{
    "match_percentage": 0,
    "missing_elements": [],
    "improvement_suggestions": {{}}
}}
"""


def parse_analysis_response(
    response_text: str,
) -> dict[str, Any]:

    cleaned = response_text.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    )

    try:
        result = json.loads(cleaned)

    except json.JSONDecodeError:

        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "Ollama did not return valid JSON."
            )

        try:
            result = json.loads(
                cleaned[start:end + 1]
            )

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Could not parse Ollama's JSON response."
            ) from exc

    if not isinstance(result, dict):
        raise ValueError(
            "Analysis result must be a JSON object."
        )

    validate_analysis_result(result)

    return result


def validate_analysis_result(
    result: dict[str, Any],
) -> None:

    required_fields = {
        "match_percentage",
        "missing_elements",
        "improvement_suggestions",
    }

    missing_fields = (
        required_fields - result.keys()
    )

    if missing_fields:
        raise ValueError(
            "Missing fields in AI response: "
            + ", ".join(
                sorted(missing_fields)
            )
        )

    percentage = result[
        "match_percentage"
    ]

    if (
        isinstance(percentage, bool)
        or not isinstance(
            percentage,
            (int, float),
        )
    ):
        raise ValueError(
            "match_percentage must be a number."
        )

    if not 0 <= percentage <= 100:
        raise ValueError(
            "match_percentage must be between 0 and 100."
        )

    missing_elements = result[
        "missing_elements"
    ]

    if not isinstance(
        missing_elements,
        list,
    ):
        raise ValueError(
            "missing_elements must be a list."
        )

    if not all(
        isinstance(item, str)
        for item in missing_elements
    ):
        raise ValueError(
            "Every missing element must be a string."
        )

    suggestions = result[
        "improvement_suggestions"
    ]

    if not isinstance(
        suggestions,
        dict,
    ):
        raise ValueError(
            "improvement_suggestions must be an object."
        )