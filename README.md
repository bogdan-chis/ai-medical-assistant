# 🤖 AI Research Assistant

A web-based platform for exploring academic and scientific literature using LLMs + RAG. Ask questions and get answers that are grounded in real papers, filtered for toxicity and hallucination risk.

Inspired by [Consensus.app](https://consensus.app).

---

## 📌 Features

- 🔍 Vector database (ChromaDB, FAISS, etc.) for semantic search
- 🧠 Local LLM integration via [LM Studio](https://lmstudio.ai)
- ⚙️ RAG (Retrieval-Augmented Generation) pipeline
- 🛡️ Toxicity and hallucination guardrails (Perspective API, RAG-based checks)
- 🖥️ Simple frontend in React or Streamlit

---

## 🧱 Architecture

1. User submits a query via web UI.
2. Backend performs vector search on embedded documents.
3. Relevant context + query is sent to a local LLM (via LM Studio).
4. Output is analyzed for toxicity and hallucination risks.
5. Final answer is returned with optional warnings and source citations.

---

## 📁 Project Structure

