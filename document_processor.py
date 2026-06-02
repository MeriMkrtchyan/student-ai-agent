import fitz
from typing import List

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes using PyMuPDF."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    parts = [page.get_text() for page in doc]
    doc.close()
    return "\n".join(parts)

def extract_text_from_txt(file_bytes: bytes) -> str:
    """Decode TXT bytes to string."""
    return file_bytes.decode("utf-8", errors="replace")

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks for semantic search."""
    if not text:
        return []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end - overlap
        
        if start < 0 or start >= len(text) - overlap:
            break
    
    return chunks
