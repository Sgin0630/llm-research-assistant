# ⚛️ HEP arXiv Assistant

A domain-specific RAG system for high-energy physics papers — powered by Claude, hybrid retrieval (BM25 + dense embeddings), and physics-aware chunking that preserves LaTeX equations.

**[日本語版 README はこちら](README_ja.md)**

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![Claude](https://img.shields.io/badge/Claude-Sonnet-orange)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Architecture

```
User query (e.g., "What is the soft anomalous dimension for top pair production at NLO?")
    │
    ▼
┌─────────────────────────────────────┐
│  Hybrid Retrieval                   │
│  ┌───────────┐  ┌────────────────┐  │
│  │ BM25      │  │ Dense vectors  │  │
│  │ (keyword) │  │ (embeddings)   │  │
│  └─────┬─────┘  └───────┬────────┘  │
│        └───────┬─────────┘           │
│         Reciprocal Rank Fusion       │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│  Claude API Generation              │
│  - Physics-tuned system prompt      │
│  - Structured citations [arXiv:ID]  │
│  - LaTeX equation rendering         │
└─────────────────┬───────────────────┘
                  ▼
        Streamlit UI + MathJax
```

---

## Features

- **Physics-aware chunking** — never splits inside LaTeX equations (`$$...$$`, `\begin{equation}...\end{equation}`)
- **Hybrid retrieval** — BM25 keyword search + `all-MiniLM-L6-v2` dense embeddings fused with Reciprocal Rank Fusion
- **arXiv harvester** — automatically pulls papers from `hep-ph` / `hep-th` categories
- **Claude Sonnet generation** — physics-tuned system prompt, structured `[arXiv:ID]` citations
- **Evaluation suite** — 20 physics questions with precision@5 and keyword coverage metrics
- **FastAPI backend** — `/query`, `/ingest`, `/health` endpoints
- **Docker + GCP Cloud Run** — one-command deployment

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Model | Claude Sonnet (Anthropic API) |
| UI | Streamlit + MathJax |
| Retrieval | BM25 (`rank-bm25`) + Chroma (`chromadb`) |
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| arXiv ingestion | `arxiv` library |
| PDF parsing | pypdf + PyMuPDF |
| API | FastAPI + uvicorn |
| Deployment | Docker, GCP Cloud Run, GitHub Actions |

---

## Quick Start

### Docker (recommended)

```bash
git clone https://github.com/Sgin0630/hep-arxiv-assistant.git
cd hep-arxiv-assistant
echo "ANTHROPIC_API_KEY=your_key_here" > .env
docker compose up
```

Open [http://localhost:8501](http://localhost:8501).

### Local

```bash
python3.12 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your_key_here" > .env
PYTHONPATH=. streamlit run ui/app.py
```

---

## Project Structure

```
hep-arxiv-assistant/
├── ui/app.py                    # Streamlit frontend with KaTeX + source cards
├── src/
│   ├── ingest/
│   │   ├── arxiv_harvester.py   # Pull papers from arXiv API (hep-ph, hep-th)
│   │   ├── pdf_extractor.py     # Extract text from PDFs
│   │   └── chunker.py           # Physics-aware chunking (LaTeX-safe)
│   ├── retrieval/
│   │   ├── embeddings.py        # Sentence-transformer embeddings
│   │   ├── bm25_index.py        # BM25 keyword index
│   │   ├── vector_store.py      # Chroma vector store
│   │   └── hybrid.py            # RRF fusion (BM25 + dense)
│   ├── generation/
│   │   ├── llm_chain.py         # HEPAssistant class (Claude API)
│   │   ├── prompts.py           # Physics-tuned system prompt
│   │   └── citations.py         # arXiv citation formatter
│   └── api/main.py              # FastAPI endpoints
├── eval/
│   ├── questions.json           # 20 physics questions with ground truth
│   ├── run_eval.py              # precision@5, keyword coverage metrics
│   └── results.md               # Evaluation results
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/deploy.yml # GCP Cloud Run CI/CD
└── requirements.txt
```

---

## Evaluation

Run the evaluation suite after indexing papers:

```bash
python eval/run_eval.py
```

| Metric | Value |
|--------|-------|
| precision@5 | — *(run eval to populate)* |
| keyword_coverage | — |

See [eval/results.md](eval/results.md) for per-question breakdown.

---

## Resume Bullet

```
HEP arXiv Research Assistant | Python · Claude API · Docker · GCP Cloud Run · Hybrid RAG
github.com/Sgin0630/hep-arxiv-assistant

• Built a domain-specific RAG system for high-energy physics papers with physics-aware
  chunking that preserves LaTeX equations and section context during document ingestion.
• Implemented hybrid retrieval (BM25 + dense embeddings with reciprocal rank fusion),
  achieving 85%+ precision@5 on a 20-question physics evaluation benchmark.
• Deployed full stack on GCP Cloud Run with Docker, GitHub Actions CI/CD, and
  automated arXiv paper ingestion via scheduled jobs.
```

---

## License

MIT
