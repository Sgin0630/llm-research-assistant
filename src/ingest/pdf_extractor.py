from src.pdf_reader import extract_text_from_pdf


def extract_text(pdf_path: str) -> str:
    """Extract all text from a PDF file using pypdf."""
    return extract_text_from_pdf(pdf_path)
