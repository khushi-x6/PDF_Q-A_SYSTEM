# qa_engine.py

from llama_cpp import Llama
import os

MODEL_PATH = "./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
llm = None  # Global LLM object

def get_llm():
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model not found at {MODEL_PATH}. Please place mistral GGUF file in /models folder.")

    global llm
    if llm is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"❌ Mistral model file not found at {MODEL_PATH}")
        llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=2048,
            n_threads=8,
            verbose=False
        )
    return llm

def format_prompt(context, question):
    return f"""[INST] Use the PDF context below to answer the question. If not found, say "I don't know".

Context:
{context}

Question: {question}
Answer:[/INST]"""

def generate_answer(context_chunks, question):
    context_text = "\n".join([chunk['content'] for chunk in context_chunks])
    prompt = format_prompt(context_text, question)
    llm_instance = get_llm()
    output = llm_instance(prompt, max_tokens=256, stop=["</s>"])
    return output['choices'][0]['text'].strip()
