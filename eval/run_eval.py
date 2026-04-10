"""
Evaluation script for HEP arXiv Assistant.

Usage:
    python eval/run_eval.py

Requires a HybridRetriever to be initialized with indexed chunks.
Results are printed to stdout and written to eval/results.md.
"""
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def evaluate(retriever, questions: list[dict]) -> dict:
    """
    Measure retrieval quality over a set of physics questions.

    Metrics:
    - precision@5: fraction of questions where expected_arxiv is in top-5 results
    - keyword_coverage: average fraction of expected_keywords found in retrieved text
    """
    results = []
    for q in questions:
        retrieved = retriever.retrieve(q["question"], top_k=5)
        retrieved_ids = [r.get("arxiv_id", "") for r in retrieved]

        hit = 1 if q["expected_arxiv"] in retrieved_ids else 0

        all_text = " ".join(r.get("text", "") for r in retrieved).lower()
        kw_hits = sum(1 for kw in q["expected_keywords"] if kw.lower() in all_text)
        kw_coverage = kw_hits / len(q["expected_keywords"]) if q["expected_keywords"] else 0.0

        results.append({
            "question": q["question"][:60] + "…",
            "expected_arxiv": q["expected_arxiv"],
            "hit": hit,
            "kw_coverage": round(kw_coverage, 2),
        })

    precision = sum(r["hit"] for r in results) / len(results)
    avg_kw = sum(r["kw_coverage"] for r in results) / len(results)
    return {
        "precision@5": round(precision, 3),
        "keyword_coverage": round(avg_kw, 3),
        "per_question": results,
    }


def write_results_md(metrics: dict, output_path: str = "eval/results.md") -> None:
    """Write evaluation results to a Markdown table."""
    lines = [
        "# Evaluation Results\n",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| precision@5 | {metrics['precision@5']} |",
        f"| keyword_coverage | {metrics['keyword_coverage']} |",
        "",
        "## Per-Question Results\n",
        "| Question | Expected arXiv | Hit | KW Coverage |",
        "|----------|---------------|-----|-------------|",
    ]
    for r in metrics["per_question"]:
        lines.append(
            f"| {r['question']} | {r['expected_arxiv']} | {'✅' if r['hit'] else '❌'} | {r['kw_coverage']} |"
        )
    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Results written to {output_path}")


if __name__ == "__main__":
    questions_path = Path(__file__).parent / "questions.json"
    with open(questions_path) as f:
        questions = json.load(f)

    print("Loading retriever… (set up your retriever here)")
    print("This script requires a HybridRetriever instance with indexed chunks.")
    print("Example usage in code:\n")
    print("  from eval.run_eval import evaluate, write_results_md")
    print("  metrics = evaluate(retriever, questions)")
    print("  write_results_md(metrics)")
    print(f"\n{len(questions)} questions loaded from {questions_path}")
