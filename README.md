# Resume-to-JD Analyzer

An AI-powered application that analyzes resumes against a job description using Ollama. It helps candidates understand how well their resumes match a target role, identify missing requirements, and improve their applications.

## Features

* Select multiple resumes using a file picker.
* Select one job description.
* Supports PDF and DOCX files.
* Validates file format, existence, and size.
* Maximum file size of 5 MB per file.
* Extracts text from resumes and job descriptions.
* Uses Ollama for AI-powered resume analysis.
* Generates a match percentage for each resume.
* Identifies missing skills, tools, qualifications, and requirements.
* Provides actionable improvement suggestions.
* Displays structured JSON results.
* Compares multiple resumes based on their match percentage.

## How It Works

1. Select one or more resume files.
2. Select a job description file.
3. The application extracts text from the selected documents.
4. Each resume is compared against the job description.
5. Ollama analyzes the resume and returns structured JSON.
6. The application displays:

   * Match percentage
   * Missing elements
   * Improvement recommendations
7. A final comparison ranks the resumes by match percentage.

## Project Structure

```text
resume_analyzer/
│
├── resume_analyzer.py       # Main application
├── ollama_client.py         # Ollama API integration
├── system_prompt.py         # AI system prompt
├── analyzer.py              # Prompt construction and JSON validation
├── file_utils.py            # File selection, validation, and text extraction
├── formatter.py             # Output formatting
├── .env                     # Environment configuration
├── .gitignore
├── requirements.txt
└── README.md
```

## Technologies Used

* **Python 3**
* **Ollama** — AI model integration
* **Requests** — API communication
* **Tkinter** — File picker
* **PyPDF** — PDF text extraction
* **python-docx** — DOCX text extraction
* **python-dotenv** — Environment variable management
* **JSON** — Structured AI responses

## Important Notes

* The match percentage is an AI-generated estimate, not a guaranteed hiring score.
* The analyzer uses information explicitly available in the resume.
* Scanned PDFs may require OCR before text can be extracted.
* Do not upload sensitive personal information unnecessarily.
* Keep API keys and private configuration files out of version control.

## Future Improvements

* Add a graphical user interface.
* Support additional document formats.
* Add OCR for scanned PDFs.
* Export analysis results to PDF or Excel.
* Add keyword-level matching and scoring.
* Support multiple AI providers.
* Add a web interface using FastAPI or Streamlit.
* Store and compare historical analysis results.

