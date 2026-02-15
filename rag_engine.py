# rag_engine.py
from pathlib import Path

RAG_PATH = Path("rag_data/medical_knowledge.txt")

def load_rag_context():
    if not RAG_PATH.exists():
        return ""
    return RAG_PATH.read_text(encoding="utf-8")
