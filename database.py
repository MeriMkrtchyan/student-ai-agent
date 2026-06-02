import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
import uuid
from document_processor import chunk_text

# Use ChromaDB's built-in lightweight embedding (ONNX, ~20MB, no PyTorch)
_embedder = DefaultEmbeddingFunction()

# Persistent storage
_chroma_client = chromadb.PersistentClient(path="./chroma_db")
_collection = _chroma_client.get_or_create_collection(
    "student_docs",
    embedding_function=_embedder
)

def add_document(filename: str, text: str) -> int:
    """Chunk text, embed, and store in ChromaDB. Returns number of chunks."""
    chunks = chunk_text(text)
    if not chunks:
        return 0
    
    ids = [f"{filename}_{uuid.uuid4().hex[:8]}" for _ in chunks]
    metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]
    
    # DefaultEmbeddingFunction handles embedding internally
    _collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )
    return len(chunks)

def search_documents(query: str, n_results: int = 3) -> str:
    """Semantic search over uploaded documents."""
    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents"]
    )
    
    docs = results.get("documents", [[]])[0]
    if not docs:
        return "No relevant content found in uploaded documents."
    
    return "\n\n---\n\n".join(docs)
