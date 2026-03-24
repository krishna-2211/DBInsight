import streamlit as st
from dotenv import load_dotenv

from utils.loaders import load_documents
from utils.vectorstore import create_vectorstore, load_vectorstore
from utils.rag_chain import answer_question

load_dotenv()

st.set_page_config(page_title="DBInsight", page_icon="🛡️")

st.title("🛡️ DBInsight")
st.markdown(
"""
A Retrieval-Augmented Generation assistant for understanding legacy SQL documentation.

Ask questions about tables, stored procedures, dependencies, and system risks.
"""
)

# Session state setup
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None


# Sidebar
st.sidebar.header("Knowledge Base")

if st.sidebar.button("Index Documents"):
    with st.spinner("Loading and indexing documents..."):
        try:
            docs = load_documents("data")
            vectorstore = create_vectorstore(docs, persist_directory="chroma_db")

            st.session_state.vectorstore = vectorstore

            st.sidebar.success(f"Indexed {len(docs)} documents.")

        except Exception as e:
            st.sidebar.error(f"Indexing failed: {e}")


if st.sidebar.button("Load Existing Index"):
    try:
        vectorstore = load_vectorstore("chroma_db")
        st.session_state.vectorstore = vectorstore

        st.sidebar.success("Vector database loaded.")

    except Exception as e:
        st.sidebar.error(f"Could not load vector store: {e}")


if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
question = st.chat_input("Ask a question about the SQL system...")

if question:

    if st.session_state.vectorstore is None:
        st.error("Please index or load the knowledge base first.")
        st.stop()

    # Show user message
    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                answer, sources = answer_question(
                    question,
                    st.session_state.vectorstore,
                    st.session_state.messages,
                )

                st.markdown(answer)

                if sources:
                    st.markdown("**Sources:**")
                    for s in sources:
                        st.markdown(f"- {s}")

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Error generating answer: {e}")