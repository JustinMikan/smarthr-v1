# SmartHR Technical Specification

## 1. Project Overview (專案概述)
- **Goal**: Build a Local RAG (Retrieval-Augmented Generation) system for querying employee handbooks.
- **User Story**: As an employee, I want to ask natural language questions about company policies and receive accurate answers cited from PDF documents.

## 2. Technology Stack (技術堆疊)
- **Language**: Python 3.10+
- **Frontend**: Streamlit (Simple Web Interface)
- **Orchestration**: LangChain (Community version)
- **Vector Database**: ChromaDB (Local persistence, no server required)
- **LLM**: Anthropic Claude 3.5 Sonnet (via API)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (HuggingFace local model)

## 3. Core Architecture (核心架構)
### Phase 1: Ingestion (資料消化)
1. Load PDF documents from `data/` directory.
2. Split text into chunks (Size: 1000 characters, Overlap: 200).
3. Generate embeddings locally.
4. Store vectors in `./chroma_db` folder.

### Phase 2: Retrieval & Generation (檢索與生成)
1. Accept user question via Streamlit input.
2. Convert question to embedding.
3. Query ChromaDB for top 3 relevant chunks.
4. Construct prompt: "Context: {chunks} Question: {question}".
5. Display answer and source documents.
