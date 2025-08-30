# Marketing Content Generator (Streamlit + LangChain Groq)

A simple and professional app to generate marketing content with streaming.

## Features
- Modular architecture (config, prompts, llm, UI)
- Typing and dataclasses
- Token-by-token streaming
- Environment variable validation
- Sidebar for quick model adjustments

## Requirements
- Python 3.10+

## Installation
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -U pip
pip install -e .
cp .env.example .env  # fill in your keys

## RUN
streamlit run app/streamlit_app.py
