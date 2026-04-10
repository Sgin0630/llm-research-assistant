import re

LATEX_BLOCK = re.compile(
    r'(\$\$.*?\$\$|\\begin\{(equation|align|eqnarray)\}.*?\\end\{\2\})',
    re.DOTALL
)


def physics_chunk(text: str, max_chunk: int = 1000, overlap: int = 200) -> list[dict]:
    """
    Chunk text while keeping LaTeX equations attached to surrounding context.
    Never split in the middle of a LaTeX block.
    Returns list of dicts: {id, text, start, end}
    """
    protected = [(m.start(), m.end()) for m in LATEX_BLOCK.finditer(text)]
    chunks = []
    start = 0
    chunk_id = 0
    while start < len(text):
        end = min(start + max_chunk, len(text))

        # Don't split inside a LaTeX block
        for block_start, block_end in protected:
            if start < block_end and end > block_start and end < block_end:
                end = block_end  # extend to include full equation

        # Try to break at paragraph boundary
        para_break = text.rfind("\n\n", start, end)
        if para_break > start + max_chunk // 2:
            end = para_break

        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append({"id": str(chunk_id), "text": chunk_text, "start": start, "end": end})
            chunk_id += 1
        start = end - overlap

    return chunks
