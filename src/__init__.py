"""
Tarih Bilgi Rehberi Chatbot Package
RAG tabanlı Türk Tarihi bilgi asistanı
"""

__version__ = "1.0.0"
__author__ = "Akbank GenAI Bootcamp"
__description__ = "RAG-based Turkish History information chatbot"

# Import ana modülleri
from .rag_system import RAGSystem
from .retrieval import FAISSRetriever
from .utils import (
    clean_text,
    Timer,
    SimpleLogger,
    ensure_dir
)

__all__ = [
    'RAGSystem',
    'FAISSRetriever',
    'clean_text',
    'Timer',
    'SimpleLogger',
    'ensure_dir'
]