import os
import PyPDF2
from shared.logger import setup_logger

logger = setup_logger(__name__)

def load_txt(file_path: str) -> str:
    """
    Loads text from a .txt file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The content of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error loading TXT file {file_path}: {e}")
        return ""

def load_pdf(file_path: str) -> str:
    """
    Extracts text from a .pdf file using PyPDF2.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text.
    """
    try:
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        logger.error(f"Error loading PDF file {file_path}: {e}")
        return ""
