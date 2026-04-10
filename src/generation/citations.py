import re


def format_citations(response: str, source_docs: list[dict]) -> str:
    """Replace bare arXiv IDs in the response with clickable Markdown links."""
    for doc in source_docs:
        arxiv_id = doc.get("arxiv_id", "")
        if not arxiv_id:
            continue
        link = f"[{arxiv_id}](https://arxiv.org/abs/{arxiv_id})"
        # Replace [arXiv:ID] style and bare ID occurrences
        response = re.sub(
            r'\[arXiv:' + re.escape(arxiv_id) + r'\]',
            f"[arXiv:{arxiv_id}]({link})",
            response,
        )
        response = response.replace(arxiv_id, link)
    return response
