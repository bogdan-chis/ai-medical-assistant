# Dr. Dialogue 🤖🏥

> **A medical‐domain conversational assistant** powered by retrieval‐augmented generation (RAG) over a curated doctor–patient dialogue dataset, with answer evaluation via a secondary LLM. 💬📚

---

## 🧐 Project Overview

**Dr. Dialogue** began as a generic research‐assistant framework but has been specialized into a **medical assistant**. It leverages a locally hosted LLM (via LM Studio) and a doctor–patient conversation dataset to answer user (patient) queries with contextually relevant, up‐to‐date medical information. All answers are then run through a secondary “DeepEval” LLM to ensure consistency, accuracy, and safety before returning to the user. 🔒✅

---

## ✨ Features

- **🔍 Retrieval‐Augmented Generation (RAG):**  
  - Ingests and preprocesses raw doctor–patient transcripts.  
  - Splits and embeds each chunk with a local embeddings service.  
  - Stores embeddings in ChromaDB for fast nearest‐neighbor lookups.  
  - Retrieves the most relevant snippets at query time and supplies them as context to the LLM.

- **🏥 Local LLM Hosting:**  
  - **Primary LLM** (e.g., a fine‐tuned medical model) runs on a local LM Studio instance.  
  - **Secondary LLM (DeepEval)** also hosted locally to evaluate clarity, quality, and safety of each generated response.

- **⚙️ FastAPI Backend:**  
  - Exposes REST endpoints for ingestion, querying, and evaluation.  
  - Manages ingestion triggers, embedding calls, RAG orchestration, and evaluation pipelines.

- **🖥️ React Frontend:**  
  - Provides a simple chat interface for end‐users (patients).  
  - Sends user queries over HTTP, receives and displays filtered, LLM‐generated medical guidance.

- **🛡️ Safety & Guardrails:**  
  - Integrates Perspective API to filter responses for harmful or disallowed content.  
  - Maintains custom prompt‐engineering templates and guardrails for medical disclaimers.

---

## 🏗️ Architecture

```text
+-------------------------------------------------------------+
|                         Frontend Layer                      |
|  ┌───────────────────────────────────────────────────────┐  |
|  | React UI  <─── HTTP: Query/Response ──  HTTP Wrappers |  |
|  └───────────────────────────────────────────────────────┘  |
|                              │                              |
|                              ▼                              |
|                     ┌───────────────────┐                   |
|                     │  API Server       │                   |
|                     │  (FastAPI)         │◀─┐              |
|                     └───────────────────┘  │                |
+-------------------------------------------------------------+
          │            ▲                      │
          │            │                      │
          │         Trigger                   │
          │         Ingestion                 │
          ▼            │                      │
┌───────────────────────────────────┐         │
│       Ingestion & Preprocessing   │         │
│  ┌─────────────┐    ┌───────────┐  │         │
│  │Dataset      │──▶ │Document   │──┼─────────┘
│  │Loader       │    │Splitter   │◀─┘
│  └─────────────┘    └───────────┘
│         │                  │
│         ▼                  ▼
│   Postprocessing        ┌──────────────┐
│         │              │ Embeddings   │
│         │─────────────▶│ Service      │
│                        └──────────────┘
│                                │
└────────────────────────────────┤
       Query Embeddings          │
                                ▼
                          ┌───────────────┐
                          │Vector Store   │
                          │Interface      │───┐
                          └───────────────┘   │
                                  │           │
                                  ▼           │
                           Retrieve Context    │
                                  │           │
                                  ▼           │
                             ┌───────────┐     │
                             │   RAG     │─────┘
                             │ Service   │
                             └───────────┘
                                  │
                     ┌────────────┴────────────┐
                     │                         │
                ┌──────────┐             ┌────────────┐
                │ LLM      │             │ DeepEval   │
                │ Client   │             │ Client     │
                └──────────┘             └────────────┘
                     │                         │
                     │                         │
             (Response from LLM)        (Evaluation Score)
                     │                         │
                     └────────────┬────────────┘
                                  ▼
                            Final Response
