# Multi-Agent AI Research Assistant

A research application that coordinates specialized AI agents to collect web
sources, analyze findings, draft a report, and review it for quality. The
project provides a FastAPI backend, a Streamlit interface, and an automated
test suite.

## Problem Statement

Research often requires searching across sources, comparing findings, writing
structured summaries, and checking claims before sharing a report. This project
automates that workflow with a sequence of focused agents and a review-and-revision
loop.

The generated report is an aid to research, not a substitute for checking
important claims against their original sources.

## Features

- Search the web with Tavily and organize source results.
- Analyze findings for trends, contradictions, knowledge gaps, and conclusions.
- Generate a structured Markdown research report.
- Review reports and revise rejected drafts, up to two revisions.
- Access the workflow through a FastAPI endpoint or Streamlit UI.
- Download the final report as a Markdown file.
- Run automated tests without Groq or Tavily API calls; external agent
  dependencies are mocked.

## Multi-Agent Architecture

```text
Research topic
    |
    v
Research Agent -- Tavily search + Groq-organized research notes
    |
    v
Analysis Agent -- findings, trends, contradictions, and gaps
    |
    v
Content Agent -- structured report draft
    |
    v
Quality Review Agent -- approval decision and feedback
    |                         |
    | approved                | rejected, fewer than 2 revisions
    v                         +------> Content Agent
Final report
```

The workflow is implemented with LangGraph. If a report is rejected, the
feedback is passed back to the Content Agent. The workflow stops when the
reviewer approves the report or the revision limit is reached.

## Technology Stack

- Python
- LangChain and LangChain-Groq
- LangGraph
- Groq API for language-model calls
- Tavily API for web search
- FastAPI and Uvicorn
- Streamlit
- Pytest and HTTPX

## Project Structure

```text
multi-agent-research-assistant/
├── agents/                 # Research, analysis, content, and review agents
├── api/                    # FastAPI application and endpoints
├── frontend/               # Streamlit application
├── graph/                  # LangGraph state and workflow
├── outputs/                # Generated reports; ignored by Git
├── scripts/                # Command-line entry points
├── tests/                  # Automated tests
├── tools/                  # Tavily web-search integration
├── .env.example            # Safe environment-variable template
├── .gitignore
├── llm_config.py           # Groq model configuration
├── pytest.ini
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10 or newer
- Git
- A Groq API key
- A Tavily API key

The live research workflow uses external APIs and requires valid keys. API
availability, rate limits, and usage terms are determined by those providers.

## Installation

In Windows PowerShell, clone the repository and create a virtual environment:

```powershell
git clone https://github.com/HarshikReddyDendi/multi-agent-research-assistant.git
Set-Location multi-agent-research-assistant
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the `py` launcher is unavailable, use `python -m venv venv` instead.

## Environment Variables

Create a local `.env` file from the safe template:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and replace the placeholders with your own credentials:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
MODEL_NAME=openai/gpt-oss-120b
```

Never commit `.env`, paste credentials into issues or logs, or share them in
screenshots. The repository's `.gitignore` excludes `.env`; `.env.example`
contains placeholders only.

## Run FastAPI

From the project root, activate the virtual environment and start the backend:

```powershell
.\venv\Scripts\Activate.ps1
uvicorn api.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API
documentation is at `http://127.0.0.1:8000/docs`, and the health endpoint is
`http://127.0.0.1:8000/health`.

The `POST /research` endpoint accepts a topic from 5 to 500 characters:

```json
{
  "topic": "Impact of generative AI on software engineering"
}
```

## Run Streamlit

Keep the FastAPI backend running, open a second PowerShell window in the
project root, activate the same environment, then start the frontend:

```powershell
.\venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

The Streamlit app connects to `http://127.0.0.1:8000` and is usually available
at `http://localhost:8501`.

## Example Research Workflow

1. Start the FastAPI backend and Streamlit frontend.
2. Enter a research topic in the Streamlit app and select **Start Research**.
3. The Research Agent searches for sources and prepares research notes.
4. The Analysis Agent identifies findings, trends, contradictions, and gaps.
5. The Content Agent drafts a structured report.
6. The Quality Review Agent approves the report or sends feedback for a
   revision (up to two revisions).
7. Review the report and status in the UI, then download the Markdown report.

The workflow can also be called directly:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/research" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"topic":"Impact of generative AI on software engineering"}'
```

## Run Tests

From the project root with the virtual environment active:

```powershell
python -m pytest -q
```

The automated tests mock agent dependencies, so they do not need API keys or
consume Groq/Tavily API usage. The file `tests/test_llm_connection.py` is a
manual live Groq smoke test when run directly; do not run it if you want to
avoid external API calls.

## Screenshots

Screenshots will be added here after the application UI is captured. Store
image files in a `docs/images/` directory and embed them in this section.

## Future Improvements

- Add screenshots and a short application walkthrough.
- Make the frontend API URL configurable for deployment.
- Add persistent storage for research history and reports.
- Add structured logs, tracing, and clearer operational error reporting.
- Expand evaluation for source quality and factual support.
- Add deployment configuration and CI for automated test runs.