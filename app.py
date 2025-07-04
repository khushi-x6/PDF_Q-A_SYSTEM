import streamlit as st
import os

from ingestion import extract_text_from_pdf
from embedder import get_embeddings
from vector_store import FaissStore
from qa_engine import generate_answer
from audio_input import record_and_transcribe

st.set_page_config(page_title="🧠 PDF Q&A Bot", layout="wide")
st.title("📘 AI-Powered PDF Q&A System")

store = FaissStore(dim=384)

st.success("📤 Upload PDFs below")
uploaded_files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded.")
    store = FaissStore(dim=384)  # recreate fresh store

    for file in uploaded_files:
        file_path = os.path.join("static/uploaded_pdfs", file.name)
        with open(file_path, 'wb') as f:
            f.write(file.read())

        store.remove_by_pdf(file.name)
        chunks = extract_text_from_pdf(file_path)
        texts = [chunk['content'] for chunk in chunks]
        embeddings = get_embeddings(texts)
        metadata = [chunk['metadata'] for chunk in chunks]
        store.add(embeddings, metadata)
        st.success("✅ Ready for questions!")


# ✅ Voice button
use_voice = st.button("🎙 Voice Query")
question = ""
if use_voice:
    question = record_and_transcribe()
    if not question or "couldn't understand" in question or question.strip() == "":
        question = ""
        st.warning("❌ Voice input failed. Please try typing instead.")

    st.success("🎤 You said:", question)
else:
    question = st.text_input("💬 Ask a question:")

if question:
    st.success(f"❓ Question received: {question}")
    query_embed = get_embeddings([question])[0]
    results = store.search(query_embed, top_k=5)

    if not results:
        st.warning("⚠️ No matching chunks found.")
    else:
        st.success("✅ Matching chunks found.")

        unique_chunks = []
        seen_texts = set()
        for meta, _ in results:
            snippet = meta['text_snippet']
            if snippet not in seen_texts:
                seen_texts.add(snippet)
                unique_chunks.append({
                    "content": snippet,
                    "pdf": meta['pdf'],
                    "page": meta['page']
                })

        context_chunks = unique_chunks

    st.markdown("##### Retrieved Context Chunks:")
    for i, chunk in enumerate(context_chunks):
        st.markdown(f"{i+1}. {chunk['content'][:200]}...")
    try:
        answer = generate_answer(context_chunks, question).strip()
        if not answer or "i don't know" in answer.lower() or "I don't know" in answer:
         answer = "⚠️ Sorry, I couldn't find a relevant answer in the provided documents."

    except Exception as e:
        answer = f"⚠️ Error while generating answer: {e}"


        st.markdown(f"""
        <div style="background-color:#f0f2f6;padding:1em;border-radius:10px">
        <strong>🤖 Answer:</strong><br><br>{answer}</div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🔍 Sources:")
        for meta, _ in results:
            st.markdown(f"""
            <div style="background-color:#eef;padding:0.5em;border-radius:8px;margin:5px 0;">
            📄 <b>{meta['pdf']}</b> | Page: <b>{meta['page']}</b><br>
            <code>{meta['text_snippet']}</code>
            </div>
            """, unsafe_allow_html=True)

