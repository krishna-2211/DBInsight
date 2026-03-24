DBInsight

DBInsight is a domain-specific Retrieval-Augmented Generation (RAG) assistant designed to help engineers understand and navigate legacy SQL documentation. The system indexes database documentation into a vector database and allows users to ask natural language questions about tables, stored procedures, dependencies, and system workflows.

This project was built as part of a class assignment to demonstrate a working RAG pipeline that includes:

A vector database

At least 10 knowledge base documents

Multi-turn conversation memory

Error handling

An interactive application interface

Project Overview

Legacy SQL systems often accumulate years of undocumented logic and dependencies. Important information may be scattered across:

Schema documentation

Stored procedures

ETL notes

Incident reports

Migration notes

Dashboard dependency files

Understanding how different parts of the system interact can be difficult and time-consuming.

DBInsight provides a conversational interface that retrieves relevant documentation and answers questions grounded in the indexed documents.

Example questions:

What is bank_routing_num used for?

What could break if bank_routing_num is renamed?

Explain the ACH payroll export process.

What documents mention payroll processing?

Key Features

Semantic document search using embeddings

Vector database powered by ChromaDB

Multi-turn conversation memory

Retrieval confidence filtering to prevent weak answers

Source attribution for transparency

Error handling for missing documents and API issues

Interactive Streamlit user interface

Technology Stack
Layer	Technology	Purpose
UI	Streamlit	Interactive chat interface
Backend	Python	Application logic
RAG Framework	LangChain	Document processing and retrieval
Vector Database	ChromaDB	Semantic document storage
Embeddings	Gemini text-embedding-004	Document vectorization
LLM (optional)	Gemini / HuggingFace	Answer generation
Environment	python-dotenv	Environment variable handling
System Architecture
Indexing Pipeline

Documents → Document Loader → Text Chunking → Embeddings → ChromaDB Vector Store

Query Pipeline

User Question → Semantic Retrieval → Confidence Check → Answer Generation / Fallback → Display Sources

How the System Works

Documents are loaded from the data/ directory.

Each document is split into smaller chunks.

Chunks are converted into embeddings using a Gemini embedding model.

Embeddings are stored in a ChromaDB vector database.

When a user asks a question, the system retrieves the most relevant document chunks.

A retrieval-confidence gate checks if the evidence is strong enough.

The system generates a response grounded in the retrieved documents.

The UI displays the answer along with the document sources.

Project Structure
DBInsight/
│
├── app.py
├── requirements.txt
├── .env
├── README.md
│
├── data/
│   ├── schema_overview.txt
│   ├── employee_bank_accounts_table.txt
│   ├── proc_generate_payroll.sql
│   ├── ach_export_process.txt
│   ├── finance_dashboard_dependencies.md
│   ├── vw_employee_payment_summary.sql
│   ├── incident_report_payroll_failure.txt
│   ├── column_migration_notes.txt
│   ├── etl_job_documentation.txt
│   └── business_glossary.txt
│
├── chroma_db/
│
└── utils/
    ├── loaders.py
    ├── vectorstore.py
    ├── rag_chain.py
    └── prompts.py
Knowledge Base

The dataset simulates documentation for a legacy payroll database system.

Included Documents

schema_overview.txt

employee_bank_accounts_table.txt

proc_generate_payroll.sql

ach_export_process.txt

finance_dashboard_dependencies.md

vw_employee_payment_summary.sql

incident_report_payroll_failure.txt

column_migration_notes.txt

etl_job_documentation.txt

business_glossary.txt

These documents cover topics such as:

payroll processing

bank routing information

ACH export workflows

dashboard dependencies

migration risks

business terminology

Setup Instructions
1. Create a Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
macOS / Linux
python3 -m venv venv
source venv/bin/activate
2. Install Dependencies
pip install -r requirements.txt
3. Create .env File

Add your API key:

GOOGLE_API_KEY=your_api_key_here
Running the Application

Start the Streamlit app:

streamlit run app.py

Open the local URL displayed in the terminal.

Example Demo Questions

You can test the system using questions such as:

What is bank_routing_num used for?

Explain the ACH payroll export process.

What could break if bank_routing_num is renamed?

What does proc_generate_payroll do?

Conversation Memory

DBInsight stores chat history using Streamlit session state.

This allows users to ask follow-up questions that depend on previous context.

Example:

User: What is bank_routing_num used for?
User: What could break if it is renamed?

The second question uses the context from the previous conversation.

Error Handling

The system gracefully handles:

Missing or unreadable documents

Empty user queries

Missing vector database

Weak retrieval results

API or model failures

If the system cannot find enough evidence in the knowledge base, it returns a safe fallback message instead of generating unsupported answers.

Assignment Requirements
Requirement	Status
Vector Database	ChromaDB
Minimum Documents	10+
Conversation Memory	Implemented
Error Handling	Implemented
Interactive System	Streamlit
Limitations

This system works only with the indexed documentation and does not connect to a live SQL database.

It does not automatically:

Detect real database dependencies

Parse SQL execution graphs

Build full lineage maps

It answers only based on the available documentation.

Future Improvements

Potential enhancements include:

Hybrid search (vector + keyword)

Query rewriting for improved retrieval

Structured summaries of retrieved documents

SQL lineage visualization

Integration with real enterprise documentation systems

Author

DBInsight was built as a course assignment by Krishna Panchal and Pralay Patil demonstrating the use of Retrieval-Augmented Generation (RAG) for understanding legacy SQL documentation.