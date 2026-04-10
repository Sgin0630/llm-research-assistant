import arxiv


def harvest_papers(categories=["hep-ph", "hep-th"], max_results=500):
    """Pull recent papers from arXiv categories."""
    client = arxiv.Client()
    for cat in categories:
        search = arxiv.Search(
            query=f"cat:{cat}",
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        for result in client.results(search):
            yield {
                "arxiv_id": result.entry_id.split("/")[-1],
                "title": result.title,
                "authors": [a.name for a in result.authors],
                "abstract": result.summary,
                "categories": result.categories,
                "published": str(result.published),
                "pdf_url": result.pdf_url,
            }
