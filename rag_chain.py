# from dotenv import load_dotenv
# load_dotenv()

# from typing import List, Tuple

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.documents import Document

# from utils.prompts import SYSTEM_PROMPT

# FAST_FAIL_MESSAGE = (
#     "I could not find enough information in the indexed documents to answer that confidently."
# )

# def format_docs(docs: List[Document]) -> str:
#     """
#     Convert retrieved documents into a readable context block.
#     """
#     formatted_chunks = []

#     for i, doc in enumerate(docs, start=1):
#         source = doc.metadata.get("source", "Unknown Source")
#         text = doc.page_content.strip()

#         formatted_chunks.append(
#             f"""Document {i}
#             Source: {source}
#             {text}"""
#         )

#     return "\n".join(formatted_chunks)



# def extract_sources(docs: List[Document]) -> List[str]:
#     """
#     Extract unique source file names from retrieved documents.
#     """
#     seen = set()
#     sources = []

#     for doc in docs:
#         source = doc.metadata.get("source", "Unknown Source")
#         if source not in seen:
#             seen.add(source)
#             sources.append(source)

#     return sources


# def build_chat_history(messages: List[dict]) -> str:
#     """
#     Convert chat history from Streamlit session format into plain text.
#     Expects messages like:
#     [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
#     """
#     history_lines = []

#     for msg in messages:
#         role = msg.get("role", "user").capitalize()
#         content = msg.get("content", "")
#         history_lines.append(f"{role}: {content}")

#     return "\n".join(history_lines)

# def _extract_text_from_response(response) -> str:
#     """
#     Safely extract text from a LangChain AIMessage response.
#     Handles both plain-string content and list-based content blocks.
#     """
#     content = response.content

#     if isinstance(content, str):
#         return content.strip()

#     if isinstance(content, list):
#         text_parts = []

#         for item in content:
#             if isinstance(item, str):
#                 text_parts.append(item)
#             elif isinstance(item, dict):
#                 # Common LangChain / provider-native block shapes
#                 if "text" in item and isinstance(item["text"], str):
#                     text_parts.append(item["text"])
#                 elif item.get("type") == "text" and isinstance(item.get("text"), str):
#                     text_parts.append(item["text"])

#         joined = "\n".join(part.strip() for part in text_parts if part and part.strip())

#         if joined:
#             return joined

#     return "I could not generate a readable answer from the model response."

# def retrieve_with_scores(question: str, vectorstore, k: int = 2):
#     """
#     Return [(Document, score), ...]
#     """
#     return vectorstore.similarity_search_with_relevance_scores(
#         question,
#         k=k,
#     )

# def is_retrieval_strong_enough(results, min_top_score: float = 0.55, min_avg_score: float = 0.45) -> bool:
#     """
#     Simple confidence gate.
#     - top result should be reasonably relevant
#     - average relevance should not be too weak
#     """
#     if not results:
#         return False

#     scores = [score for _, score in results]
#     top_score = scores[0]
#     avg_score = sum(scores) / len(scores)

#     print("\nRetrieval scores:")
#     for doc, score in results:
#         print(f"{score:.3f} | {doc.metadata.get('source', 'Unknown Source')}")

#     return top_score >= min_top_score and avg_score >= min_avg_score


# def answer_question(question: str, vectorstore, chat_history: List[dict]) -> Tuple[str, List[str]]:
#     if not question.strip():
#         raise ValueError("Question cannot be empty.")

#     results = retrieve_with_scores(question, vectorstore, k=2)

#     if not is_retrieval_strong_enough(results):
#         weak_sources = [doc.metadata.get("source", "Unknown Source") for doc, _ in results[:2]]
#         weak_sources = list(dict.fromkeys(weak_sources))
#         return FAST_FAIL_MESSAGE, weak_sources

#     docs = [doc for doc, _ in results]
#     sources = extract_sources(docs)
#     context = format_docs(docs)[:3000]
#     history_text = build_chat_history(chat_history)

#     prompt = SYSTEM_PROMPT.format(
#         context=context,
#         chat_history=history_text if history_text else "No prior conversation.",
#         question=question,
#     )

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-3-flash-preview",
#         temperature=0,
#     )

#     response = llm.invoke(prompt)
#     answer = _extract_text_from_response(response)

#     return answer, sources

from dotenv import load_dotenv
load_dotenv()

from typing import List, Tuple

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document

from utils.prompts import SYSTEM_PROMPT


FAST_FAIL_MESSAGE = (
    "I could not find enough information in the indexed documents to answer that confidently."
)

# Set this to False for demo-safe fast responses
USE_LLM = True


def format_docs(docs: List[Document]) -> str:
    formatted = []

    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "Unknown Source")
        text = doc.page_content.strip()

        formatted.append(
            f"""Document {i}
Source: {source}

{text}
"""
        )

    return "\n".join(formatted)


def extract_sources(docs: List[Document]) -> List[str]:
    seen = set()
    sources = []

    for doc in docs:
        source = doc.metadata.get("source", "Unknown Source")
        if source not in seen:
            seen.add(source)
            sources.append(source)

    return sources


def build_chat_history(messages: List[dict]) -> str:
    history_lines = []

    for msg in messages:
        role = msg.get("role", "user").capitalize()
        content = msg.get("content", "")
        history_lines.append(f"{role}: {content}")

    return "\n".join(history_lines)


def _extract_text_from_response(response) -> str:
    content = response.content

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, str):
                text_parts.append(item)
            elif isinstance(item, dict):
                if "text" in item and isinstance(item["text"], str):
                    text_parts.append(item["text"])
                elif item.get("type") == "text" and isinstance(item.get("text"), str):
                    text_parts.append(item["text"])

        joined = "\n".join(part.strip() for part in text_parts if part and part.strip())
        if joined:
            return joined

    return "I could not generate a readable answer from the model response."


def retrieve_with_scores(question: str, vectorstore, k: int = 2):
    """
    Return [(Document, score), ...]
    """
    return vectorstore.similarity_search_with_relevance_scores(
        question,
        k=k,
    )


def is_retrieval_strong_enough(
    results,
    min_top_score: float = 0.55,
    min_avg_score: float = 0.45,
) -> bool:
    """
    Confidence gate:
    - top result must be reasonably relevant
    - average relevance should not be too weak
    """
    if not results:
        return False

    scores = [score for _, score in results]
    top_score = scores[0]
    avg_score = sum(scores) / len(scores)

    print("\nRetrieval scores:")
    for doc, score in results:
        print(f"{score:.3f} | {doc.metadata.get('source', 'Unknown Source')}")

    return top_score >= min_top_score and avg_score >= min_avg_score


def build_fallback_answer(question: str, docs: List[Document]) -> str:
    """
    Build a fast retrieval-grounded answer without calling the LLM.
    """
    if not docs:
        return FAST_FAIL_MESSAGE

    intro = f"Based on the indexed documents, here is the most relevant information for your question: '{question}'\n"

    snippets = []
    for i, doc in enumerate(docs[:2], start=1):
        source = doc.metadata.get("source", "Unknown Source")
        content = " ".join(doc.page_content.strip().split())
        snippets.append(f"{i}. {content[:260]}...")

    answer = intro + "\n\n" + "\n\n".join(snippets)
    return answer


def answer_question(question: str, vectorstore, chat_history: List[dict]) -> Tuple[str, List[str]]:
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    results = retrieve_with_scores(question, vectorstore, k=2)

    if not is_retrieval_strong_enough(results):
        weak_sources = [doc.metadata.get("source", "Unknown Source") for doc, _ in results[:2]]
        weak_sources = list(dict.fromkeys(weak_sources))
        return FAST_FAIL_MESSAGE, weak_sources

    docs = [doc for doc, _ in results]
    sources = extract_sources(docs)

    # Fast demo-safe mode: retrieval-grounded answer only
    if not USE_LLM:
        answer = build_fallback_answer(question, docs)
        return answer, sources

    # Optional LLM mode
    context = format_docs(docs)[:3000]
    history_text = build_chat_history(chat_history)

    prompt = SYSTEM_PROMPT.format(
        context=context,
        chat_history=history_text if history_text else "No prior conversation.",
        question=question,
    )

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
        )

        response = llm.invoke(prompt)
        answer = _extract_text_from_response(response)

        if not answer.strip():
            answer = build_fallback_answer(question, docs)

    except Exception:
        answer = build_fallback_answer(question, docs)

    return answer, sources