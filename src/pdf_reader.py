import pypdf
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF file."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text += f"\n--- Page {i+1} ---\n{page_text}"
    
    if not text.strip():
        raise ValueError("Could not extract text from PDF. It may be scanned/image-based.")
    
    return text


def chunk_text(text: str, max_chars: int = 8000) -> list[str]:
    """Split long text into chunks on paragraph boundaries."""
    if len(text) <= max_chars:
        return [text]

    paragraphs = text.split("\n\n")
    chunks = []
    current = ""

    for para in paragraphs:
        candidate = current + ("\n\n" if current else "") + para
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)
            # If a single paragraph exceeds max_chars, split on sentence boundaries
            if len(para) > max_chars:
                sentences = para.replace(". ", ".\n").split("\n")
                current = ""
                for sentence in sentences:
                    candidate = current + (" " if current else "") + sentence
                    if len(candidate) <= max_chars:
                        current = candidate
                    else:
                        if current:
                            chunks.append(current)
                        current = sentence
            else:
                current = para

    if current:
        chunks.append(current)

    return chunks


def get_pdf_metadata(pdf_path: str) -> dict:
    """Return title, number of pages, and author from a PDF if available."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = pypdf.PdfReader(pdf_path)
    info = reader.metadata or {}

    return {
        "title": info.get("/Title") or None,
        "author": info.get("/Author") or None,
        "num_pages": len(reader.pages),
    }


def load_pdf_for_assistant(pdf_path: str) -> str:
    """Load a PDF and return text ready to pass to the assistant."""
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    
    # For now, use the first chunk (we'll improve this with the UI later)
    if len(chunks) > 1:
        print(f"Note: PDF has {len(chunks)} chunks. Using first {len(chunks[0])} chars.")
    
    return chunks[0]