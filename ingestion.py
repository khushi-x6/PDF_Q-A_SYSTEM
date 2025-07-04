import pdfplumber
import os
import uuid

def extract_text_from_pdf(file_path):
    chunks = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            try:
                text = page.extract_text() or ""
                paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
                for para in paragraphs:
                    if len(para) > 30:  # Skip very short lines
                        chunks.append({
                            "content": para,
                            "metadata": {
                                "pdf": os.path.basename(file_path),
                                "page": i + 1,
                                "text_snippet": para[:300]
                            }
                        })
            except Exception as e:
                print(f"Skipping page {i+1}: {e}")
    return chunks
