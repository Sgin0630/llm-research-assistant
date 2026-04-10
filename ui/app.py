import streamlit as st
import tempfile
import os

from src.generation.llm_chain import HEPAssistant
from src.ingest.pdf_extractor import extract_text
from src.ingest.chunker import physics_chunk

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HEP arXiv Assistant",
    page_icon="⚛️",
    layout="wide",
)

# KaTeX support via MathJax
st.markdown(
    """
    <script>
    window.MathJax = {
      tex: { inlineMath: [['$', '$']], displayMath: [['$$', '$$']] },
      startup: { ready() { MathJax.startup.defaultReady(); } }
    };
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
    """,
    unsafe_allow_html=True,
)

st.title("⚛️ HEP arXiv Assistant")
st.caption("Physics-aware RAG for high-energy physics papers · powered by Claude + hybrid retrieval")

# ── Session state ─────────────────────────────────────────────────────────────
if "assistant" not in st.session_state:
    st.session_state.assistant = HEPAssistant()  # no retriever until PDF loaded
if "messages" not in st.session_state:
    st.session_state.messages = []          # list of {role, content, sources}
if "document_loaded" not in st.session_state:
    st.session_state.document_loaded = False

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📄 Load a Paper")

    uploaded_file = st.file_uploader("Upload a PDF (arXiv paper)", type=["pdf"])

    if uploaded_file and not st.session_state.document_loaded:
        with st.spinner("Extracting and indexing paper…"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            try:
                text = extract_text(tmp_path)
                chunks = physics_chunk(text)
                # Add arxiv_id placeholder from filename (user can set later)
                arxiv_id = uploaded_file.name.replace(".pdf", "")
                for chunk in chunks:
                    chunk["arxiv_id"] = arxiv_id

                # Build in-memory retriever (no vector store for quick demo)
                from src.retrieval.bm25_index import BM25Index

                class _SimpleBM25Retriever:
                    def __init__(self, chunks):
                        self.chunks = chunks
                        self.chunk_map = {c["id"]: c for c in chunks}
                        self.index = BM25Index()
                        self.index.build(chunks)

                    def retrieve(self, query, top_k=5):
                        ids = self.index.search(query, top_k=top_k)
                        return [self.chunk_map[i] for i in ids if i in self.chunk_map]

                st.session_state.assistant.retriever = _SimpleBM25Retriever(chunks)
                st.session_state.document_loaded = True
                st.success(f"✅ Indexed {len(chunks)} chunks from {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error processing PDF: {e}")
            finally:
                os.unlink(tmp_path)

    st.divider()

    if st.button("🗑️ Clear conversation"):
        st.session_state.assistant.clear_history()
        st.session_state.messages = []
        st.session_state.document_loaded = False
        st.session_state.assistant.retriever = None
        st.rerun()

    st.divider()
    st.markdown("**Usage**")
    total_messages = len(st.session_state.messages)
    estimated_chars = sum(len(m["content"]) for m in st.session_state.messages)
    col1, col2 = st.columns(2)
    col1.metric("Messages", total_messages)
    col2.metric("Est. chars", f"{estimated_chars:,}")

    st.divider()
    st.markdown("**Suggested questions:**")
    suggestions = [
        "What is the DGLAP equation and how does it govern parton evolution?",
        "Explain the soft anomalous dimension for top quark pair production.",
        "What are the main results of this paper?",
        "Derive the leading-order cross section for this process.",
        "What are the limitations or open questions?",
    ]
    for suggestion in suggestions:
        if st.button(suggestion, use_container_width=True):
            st.session_state.pending_input = suggestion

# ── Chat history ──────────────────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander(f"📚 {len(message['sources'])} source(s)", expanded=False):
                for src in message["sources"]:
                    arxiv_id = src.get("arxiv_id", "unknown")
                    snippet = src.get("text", "")[:300].replace("\n", " ")
                    st.markdown(
                        f"**[arXiv:{arxiv_id}](https://arxiv.org/abs/{arxiv_id})**  \n"
                        f"_{snippet}…_"
                    )


def _send(prompt: str):
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Retrieving and generating…"):
            response, sources = st.session_state.assistant.chat(prompt)
        st.markdown(response)
        if sources:
            with st.expander(f"📚 {len(sources)} source(s)", expanded=False):
                for src in sources:
                    arxiv_id = src.get("arxiv_id", "unknown")
                    snippet = src.get("text", "")[:300].replace("\n", " ")
                    st.markdown(
                        f"**[arXiv:{arxiv_id}](https://arxiv.org/abs/{arxiv_id})**  \n"
                        f"_{snippet}…_"
                    )
    st.session_state.messages.append({"role": "assistant", "content": response, "sources": sources})
    st.rerun()


# Handle suggested question clicks
if "pending_input" in st.session_state:
    _send(st.session_state.pop("pending_input"))

# Chat input
if prompt := st.chat_input("Ask a physics question…"):
    _send(prompt)
