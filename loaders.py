from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


SUPPORTED_EXTENSIONS = {".txt", ".md", ".sql", ".pdf"}


def load_documents(data_dir: str = "data") -> List[Document]:
    """
    Load all supported documents from the data directory.

    Supported file types:
    - .txt
    - .md
    - .sql
    - .pdf

    Returns:
        List[Document]: Loaded LangChain documents with source metadata.

    Raises:
        FileNotFoundError: If the data directory does not exist.
        ValueError: If no supported documents are found.
    """
    data_path = Path(data_dir)

    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    documents: List[Document] = []
    supported_files = [
        file_path
        for file_path in data_path.iterdir()
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not supported_files:
        raise ValueError(
            f"No supported documents found in '{data_dir}'. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    for file_path in supported_files:
        try:
            docs = _load_single_file(file_path)

            for doc in docs:
                doc.metadata["source"] = file_path.name
                doc.metadata["file_path"] = str(file_path)

            documents.extend(docs)

        except Exception as exc:
            print(f"Skipping {file_path.name}: {exc}")

    if not documents:
        raise ValueError("Documents were found, but none could be loaded successfully.")

    return documents


def _load_single_file(file_path: Path) -> List[Document]:
    """
    Load a single file and return a list of LangChain Document objects.
    """
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
        return loader.load()

    if suffix in {".txt", ".md", ".sql"}:
        loader = TextLoader(str(file_path), encoding="utf-8")
        return loader.load()

    raise ValueError(f"Unsupported file type: {suffix}")