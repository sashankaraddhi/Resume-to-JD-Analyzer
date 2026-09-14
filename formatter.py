import json
from pathlib import Path
from typing import Any


def format_analysis_result(
    resume_path: Path,
    result: dict[str, Any],
) -> str:

    percentage = result["match_percentage"]
    missing = result["missing_elements"]
    suggestions = result[
        "improvement_suggestions"
    ]

    lines = []

    lines.append("")
    lines.append("=" * 70)
    lines.append(
        f"RESUME: {resume_path.name}"
    )
    lines.append("=" * 70)

    lines.append("")
    lines.append("┌" + "─" * 66 + "┐")
    lines.append(
        f"│  MATCH                                      {percentage:>3}%  │"
    )
    lines.append("└" + "─" * 66 + "┘")

    lines.append("")
    lines.append("┌" + "─" * 66 + "┐")
    lines.append(
        "│  MISSING ELEMENTS                           │"
    )
    lines.append("└" + "─" * 66 + "┘")

    if missing:

        for index, item in enumerate(
            missing,
            start=1,
        ):
            lines.append(
                f"  {index}. {item}"
            )

    else:
        lines.append(
            "  ✓ No important missing elements identified."
        )

    lines.append("")
    lines.append("┌" + "─" * 66 + "┐")
    lines.append(
        "│  RECOMMENDATIONS                            │"
    )
    lines.append("└" + "─" * 66 + "┘")

    if suggestions:

        for key, suggestion in suggestions.items():

            lines.append(
                f"\n  [{key.upper()}]"
            )

            lines.append(
                f"  {suggestion}"
            )

    else:
        lines.append(
            "  No specific recommendations."
        )

    return "\n".join(lines)


def format_json_output(
    result: dict[str, Any],
) -> str:

    return json.dumps(
        result,
        indent=2,
        ensure_ascii=False,
    )