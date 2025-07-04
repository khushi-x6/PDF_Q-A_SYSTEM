# 📘 AI-Powered PDF Q&A System

A lightweight, local-first AI-powered Question Answering (Q&A) system over PDF documents using embeddings, FAISS, and open-source language models.

---

## 🚀 Tech Stack Used

| Component        | Technology                          |
|------------------|--------------------------------------|
| **Frontend/UI**  | Streamlit                           |
| **PDF Parsing**  | `pdfplumber`                        |
| **Embeddings**   | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| **Vector Store** | FAISS (in-memory)                   |
| **LLM Backend**  | `llama-cpp-python` + Mistral 7B Instruct GGUF |
| **Voice Input**  | `speech_recognition` (Google Speech-to-Text) |

---

## 📂 Folder Structure

```
├── app.py
├── ingestion.py
├── embedder.py
├── vector_store.py
├── qa_engine.py
├── audio_input.py
├── models/
│   └── mistral-7b-instruct-v0.1.Q4_K_M.gguf
├── static/
│   └── uploaded_pdfs/
├── sample_pdfs/
│   └── Wireshark_DNS_Help-1.pdf
├── requirements.txt
```

---

## ⚙️ How to Run Locally

1️⃣ **Clone the Repository:**

```bash
git clone <your-repo-link>
cd <repo-folder>
```

2️⃣ **Set Up Virtual Environment (Optional but Recommended):**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3️⃣ **Install Dependencies:**

```bash
pip install -r requirements.txt
```

🔗 **Important:** Install `llama-cpp-python` properly:

```bash
pip install llama-cpp-python
```

✅ Make sure you have the **Mistral GGUF model** downloaded and placed inside the `models/` folder as:

```
models/mistral-7b-instruct-v0.1.Q4_K_M.gguf
```

4️⃣ **Run the App:**

```bash
streamlit run app.py
```

5️⃣ **Test:**
- Upload any PDF (sample PDF `Wireshark_DNS_Help-1` provided)
- Ask a question via text or click **Voice Query** to speak
- Answers + sources will appear below

---

## ⚠️ Known Issues / Limitations

- 🔄 **LLM Inference Speed:** Running Mistral-7B locally may be slow on lower-end devices.
- 🧠 **Answer Quality:** Sometimes answers may be incomplete or inaccurate if context chunks are poor.
- 📄 **Source Highlighting:** Partial; shows source snippets but doesn't highlight exact lines in PDF.
- 🔊 **Voice Input Errors:** Speech-to-text may occasionally fail; fall back to text input.
- 💾 **FAISS Persistence:** Current FAISS index is rebuilt every time — no long-term persistence between runs.

---

✅ Tested on:
- Windows 10/11
- Python 3.10+
- Streamlit 1.34+
- llama-cpp-python 0.2+

---

👉 For best performance:
- Use smaller Mistral GGUF models (Q4_K_M recommended)
- Avoid very large PDFs (>200 pages) without sufficient system RAM.

---

Thank you 🙏

