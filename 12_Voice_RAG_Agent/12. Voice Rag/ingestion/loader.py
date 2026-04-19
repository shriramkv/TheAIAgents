import os
from typing import List

def load_documents(directory_path: str) -> List[str]:
    """
    Load text documents from a directory.
    """
    documents = []
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return documents

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                documents.append(f.read())
    
    return documents
