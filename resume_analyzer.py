#!/usr/bin/env python3

import sys

from dotenv import load_dotenv

from analyzer import (
    build_analysis_prompt,
    parse_analysis_response,
)

from file_utils import (
    select_input_files,
    validate_file,
    extract_text,
)

from formatter import (
    format_analysis_result,
    format_json_output,
)

from ollama_client import OllamaClient


def main() -> int:

    load_dotenv()

    print("=" * 70)
    print("              Resume-to-JD Analyzer")
    print("=" * 70)

    try:

        # --------------------------------------------------
        # 1. Select files
        # --------------------------------------------------

        resume_inputs, jd_input = (
            select_input_files()
        )

        # --------------------------------------------------
        # 2. Validate JD
        # --------------------------------------------------

        jd_path = validate_file(
            jd_input,
            "Job description",
        )

        # --------------------------------------------------
        # 3. Validate resumes
        # --------------------------------------------------

        resume_paths = []

        for resume_input in resume_inputs:

            resume_path = validate_file(
                resume_input,
                "Resume",
            )

            resume_paths.append(
                resume_path
            )

        # --------------------------------------------------
        # 4. Extract JD
        # --------------------------------------------------

        print("\nReading job description...")

        jd_text = extract_text(
            jd_path
        )

        print(
            f"JD text extracted: "
            f"{len(jd_text):,} characters"
        )

        # --------------------------------------------------
        # 5. Create Ollama client
        # --------------------------------------------------

        ollama = OllamaClient()

        # --------------------------------------------------
        # 6. Analyze resumes
        # --------------------------------------------------

        all_results = []

        for index, resume_path in enumerate(
            resume_paths,
            start=1,
        ):

            print("\n")
            print("=" * 70)
            print(
                f"Analyzing Resume "
                f"{index}/{len(resume_paths)}"
            )
            print(
                f"File: {resume_path.name}"
            )
            print("=" * 70)

            # ----------------------------------------------
            # Extract resume
            # ----------------------------------------------

            resume_text = extract_text(
                resume_path
            )

            print(
                f"Resume text extracted: "
                f"{len(resume_text):,} characters"
            )

            # ----------------------------------------------
            # Build prompt
            # ----------------------------------------------

            prompt = build_analysis_prompt(
                resume_text,
                jd_text,
            )

            # ----------------------------------------------
            # Ollama
            # ----------------------------------------------

            raw_response = ollama.generate(
                prompt
            )

            # ----------------------------------------------
            # Parse response
            # ----------------------------------------------

            result = parse_analysis_response(
                raw_response
            )

            # ----------------------------------------------
            # Store
            # ----------------------------------------------

            all_results.append(
                {
                    "resume": resume_path.name,
                    "result": result,
                }
            )

            # ----------------------------------------------
            # Display
            # ----------------------------------------------

            print(
                format_analysis_result(
                    resume_path,
                    result,
                )
            )

            print("\n--- JSON OUTPUT ---")

            print(
                format_json_output(
                    result
                )
            )

        # --------------------------------------------------
        # 7. Final comparison
        # --------------------------------------------------

        print("\n")
        print("=" * 70)
        print("                    FINAL COMPARISON")
        print("=" * 70)

        sorted_results = sorted(
            all_results,
            key=lambda item: item["result"][
                "match_percentage"
            ],
            reverse=True,
        )

        for rank, item in enumerate(
            sorted_results,
            start=1,
        ):

            print(
                f"{rank}. "
                f"{item['resume']:<40} "
                f"Match: "
                f"{item['result']['match_percentage']}%"
            )

        print("=" * 70)

        print(
            "\nAnalysis completed successfully."
        )

        return 0

    except KeyboardInterrupt:

        print(
            "\n\nAnalysis cancelled."
        )

        return 130

    except (
        FileNotFoundError,
        ValueError,
        RuntimeError,
    ) as exc:

        print(
            f"\n❌ Error: {exc}",
            file=sys.stderr,
        )

        return 1

    except Exception as exc:

        print(
            f"\n❌ Unexpected error: {exc}",
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(main())