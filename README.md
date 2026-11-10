# Persistent Memory Agent OS

A small persistent memory service for multi-session agents. It stores episodic memories in SQLite, supports tags and session IDs, and retrieves relevant records using a transparent token-overlap baseline. Replace the retriever with embeddings/vector search as the next step.

## Run
```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
```
Data persists in `memory.db`. API docs: /docs.
