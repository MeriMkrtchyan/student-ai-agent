import chromadb
from sentence_transformers import SentenceTransformer
import uuid
from document_processor import chunk_text

# Load free local embedding model (22MB, runs on CPU)
_embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent storage — survives server restarts
_chroma_client = chromadb.PersistentClient(path="./chroma_db")
_collection = _chroma_client.get_or_create_collection("student_docs")

def add_document(filename: str, text: str) -> int:
    """Chunk text, embed, and store in ChromaDB. Returns number of chunks."""
    chunks = chunk_text(text)
    if not chunks:
        return 0
    
    ids = [f"{filename}_{uuid.uuid4().hex[:8]}" for _ in chunks]
    embeddings = _embedder.encode(chunks, show_progress_bar=False).tolist()
    metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]
    
    _collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )
    return len(chunks)

def search_documents(query: str, n_results: int = 3) -> str:
    """Semantic search over uploaded documents."""
    query_embedding = _embedder.encode([query], show_progress_bar=False).tolist()
    results = _collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents"]
    )
    
    docs = results.get("documents", [[]])[0]
    if not docs:
        return "No relevant content found in uploaded documents."
    
    return "\n\n---\n\n".join(docs)
