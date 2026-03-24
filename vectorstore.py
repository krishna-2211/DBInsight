from dotenv import load_dotenv
load_dotenv()

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


def split_documents(
    documents: List[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)


def create_vectorstore(
    documents: List[Document],
    persist_directory: str = "chroma_db",
) -> Chroma:
    if not documents:
        raise ValueError("No documents provided for vector store creation.")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    chunks = split_documents(documents)

    if not chunks:
        raise ValueError("Document splitting produced no chunks.")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
    )

    return vectorstore


def load_vectorstore(
    persist_directory: str = "chroma_db",
) -> Chroma:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )


def get_retriever(vectorstore: Chroma, k: int = 2):
    return vectorstore.as_retriever(search_kwargs={"k": k})