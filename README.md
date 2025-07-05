# Dr. Dialogue 🤖🏥

> **A medical‐domain conversational assistant** powered by retrieval‐augmented generation (RAG) over a curated doctor–patient dialogue dataset, with answer evaluation via a secondary LLM. 💬📚

---

## 🧐 Project Overview

**Dr. Dialogue**leverages a locally hosted LLM (via LM Studio) and a doctor–patient conversation dataset to answer user (patient) queries with contextually relevant, up‐to‐date medical information. All answers are then run through a secondary “DeepEval” LLM to ensure consistency, accuracy, and safety before returning to the user (also locally hosted). 🔒✅

---

## ✨ Features

* **🔍 Retrieval‐Augmented Generation (RAG):**

  * Ingests and preprocesses raw doctor–patient transcripts.
  * Splits and embeds each chunk with a local embeddings service.
  * Stores embeddings in ChromaDB for fast nearest‐neighbor lookups.
  * Retrieves the most relevant snippets at query time and supplies them as context to the LLM.

* **🏥 Local LLM Hosting:**

  * **Primary LLM** (e.g., a fine‐tuned medical model) runs on a local LM Studio instance.
  * **Secondary LLM (DeepEval)** also hosted locally to evaluate clarity, quality, and safety of each generated response.

* **⚙️ FastAPI Backend:**

  * Exposes REST endpoints for ingestion, querying, and evaluation.
  * Manages ingestion triggers, embedding calls, RAG orchestration, and evaluation pipelines.

* **🖥️ React Frontend:**

  * Provides a simple chat interface for end‐users (patients).
  * Sends user queries over HTTP, receives and displays filtered, LLM‐generated medical guidance.

* **🛡️ Safety & Guardrails:**
  
  * Maintains custom prompt‐engineering templates and guardrails for medical disclaimers.

---

## 🚀 Getting Started

Follow these steps to get **Dr. Dialogue** up and running locally.

### 1. Prerequisites

* **Python 3.8+**
* **Node.js & npm** (v14+)
* **LM Studio** installed and licensed locally

### 2. Clone the Repository

```bash
git clone https://github.com/bogdan-chis/ai-medical-assistant.git
```

### 3. Configure Environment Variables

Copy the example environment file and update necessary values:

```bash
cp .env.example .env
```

Open `.env` and set the following:

```dotenv
# --- existing RAG LLM (phi-4) ---
LLM_API_BASE_URL=http://localhost:1234/v1
LLM_API_KEY=lm-studio
LLM_MAIN_MODEL=phi-4

# --- new Judge LLM (locally-hosted) ---
JUDGE_API_BASE_URL=http://localhost:1234/v1
JUDGE_API_KEY=lm-studio
JUDGE_MODEL_PATH=phi-4
```

You can modify the LM Studio URL and both API keys here at any time.

### 4. Install Dependencies

#### Backend

```bash
pip install -r requirements.txt
```

#### Frontend

```bash
cd frontend
npm install
cd ..
```

### 5. Start the LM Studio Server

Launch your local LM Studio instance per its documentation. Once running, confirm the URL and keys match those in your `.env` file.

### 6. Run the Application

#### a. Start the Python Backend Server

From the project root:

```bash
python -m backend.api.main
```

The FastAPI server will start (default `http://127.0.0.1:8000`).

#### b. Launch the React Frontend

In a separate terminal:

```bash
cd frontend
npm.cmd start
```

This will open the web UI (usually at `http://localhost:3000`).

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
|                     └───────────────────┘    │              |
+-------------------------------------------------------------+
          │            ▲                      │
          │            │                      │
          │         Trigger                   │
          │         Ingestion                 │
          ▼            │                      │
┌─────────────────────────────────────┐       │
│       Ingestion & Preprocessing     │       │
│  ┌─────────────┐    ┌───────────┐   │       │
│  │Dataset      │──▶ │Document   │──┼───────┘
│  │Loader       │    │Splitter   │◀─┘
│  └─────────────┘    └───────────┘
│         │                  │
│         ▼                  ▼
│   Postprocessing        ┌──────────────┐
│         │               │ Embeddings   │
│         │─────────────▶│ Service      │
│                         └──────────────┘
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
                           Retrieve Context   │
                                  │           │
                                  ▼           │
                             ┌───────────┐    │
                             │   RAG     │────┘
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
```
