import chromadb
from config.settings import CHROMA_DB_DIR, COLLECTION_NAME

try:
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    col = client.get_collection(name=COLLECTION_NAME)
    print("COUNT:", col.count())
    print("DOCS:", col.get())
except Exception as e:
    print("ERROR:", e)
