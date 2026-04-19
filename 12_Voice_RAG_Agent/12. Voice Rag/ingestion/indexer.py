from ingestion.loader import load_documents
from ingestion.chunker import chunk_text
from shared.embeddings import get_embeddings
from shared.vector_store import vector_store
from shared.utils import load_config

def build_index():
    """
    Load documents, chunk them, generate embeddings, and store in FAISS.
    """
    config = load_config()
    data_path = config.get("data_path", "data/sample_docs")
    chunk_size = config.get("chunk_size", 400)

    # 1. Load
    documents = load_documents(data_path)
    if not documents:
        print("No documents found to index.")
        return

    # 2. Chunk
    all_chunks = []
    for doc in documents:
        all_chunks.extend(chunk_text(doc, chunk_size=chunk_size))

    # 3. Embed & Store
    embeddings = get_embeddings(all_chunks)
    vector_store.add_texts(all_chunks, embeddings)
    
    # 4. Save
    vector_store.save()
    print(f"Index built with {len(all_chunks)} chunks.")

if __name__ == "__main__":
    build_index()
