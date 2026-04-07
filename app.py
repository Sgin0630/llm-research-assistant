import streamlit as st
from src.assistant import ResearchAssistant
from src.pdf_reader import load_pdf_for_assistant
import tempfile
import os

# Page config
st.set_page_config(
    page_title="Research Assistant",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Research Assistant")
st.caption("Upload a research paper and chat with it using Claude AI")

# Initialize assistant in session state (persists across reruns)
if "assistant" not in st.session_state:
    st.session_state.assistant = ResearchAssistant()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "document_loaded" not in st.session_state:
    st.session_state.document_loaded = False

# Sidebar — document upload
with st.sidebar:
    st.header("📄 Load a Document")
    
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    
    if uploaded_file and not st.session_state.document_loaded:
        with st.spinner("Reading PDF..."):
            # Save to temp file so pypdf can read it
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            
            try:
                text = load_pdf_for_assistant(tmp_path)
                response = st.session_state.assistant.load_document(
                    text, source_name=uploaded_file.name
                )
                st.session_state.document_loaded = True
                st.session_state.messages.append({
                    "role": "assistant", "content": response
                })
                st.success(f"✅ Loaded: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
            finally:
                os.unlink(tmp_path)
    
    st.divider()
    
    if st.button("🗑️ Clear conversation"):
        st.session_state.assistant.clear_history()
        st.session_state.messages = []
        st.session_state.document_loaded = False
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
        "Summarize the key findings",
        "What methodology was used?",
        "What are the limitations?",
        "Explain the main conclusions",
    ]
    for suggestion in suggestions:
        if st.button(suggestion, use_container_width=True):
            st.session_state.pending_input = suggestion

# Main chat area — display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle suggested question clicks
if "pending_input" in st.session_state:
    prompt = st.session_state.pop("pending_input")
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.assistant.chat(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask anything about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.assistant.chat(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()