# AegisMind

**AegisMind** is a modular, agentic AI system built to deeply understand and demonstrate how modern **multi-agent AI architectures** work in practice. The project focuses on *orchestration, memory, retrieval, and tool-based reasoning* rather than relying on monolithic LLM behavior.

It uses the **Groq API** purely as a fast inference engine, while all intelligence — planning, routing, memory, document understanding, and tool usage — is engineered explicitly.

> **Goal:** Learn and showcase *true Agentic AI system design*, not just prompt engineering.

---

## 🚀 Core Capabilities

* **Multi-Agent Architecture**

  * Planner agent for intent detection and routing
  * Specialized agents for document Q&A, memory, voice, and tools

* **Agent Orchestration (LangGraph)**

  * Explicit state management
  * Conditional routing between agents
  * Clear separation of planning vs execution

* **Document Intelligence (RAG)**

  * Upload PDFs and documents
  * Chunking and embeddings
  * Retrieval-augmented generation for grounded answers

* **Memory System**

  * Short-term conversational memory
  * Long-term semantic memory (facts, preferences, summaries)
  * Memory write/read rules to avoid context pollution

* **Groq-powered Reasoning**

  * Uses Groq-hosted LLaMA / Mixtral models
  * Stateless inference with structured prompts

* **Voice Support (Optional Module)**

  * Speech-to-text (Whisper)
  * Text-to-speech (Piper / Coqui)

* **MCP (Model Context Protocol) Support (Advanced)**

  * MCP client integration
  * Agent-based tool invocation via MCP servers

---

## 🧠 Why AegisMind?

Most chatbot projects rely on:

* Single-agent prompts
* Implicit memory (chat history)
* Hard-coded tool calls

AegisMind is different:

* LLMs are treated as **stateless reasoning engines**
* Intelligence emerges from **system design**, not prompts
* Memory, planning, and tools are explicit, inspectable components

This mirrors how **real-world AI agent systems** are built.

---

## 🏗️ High-Level Architecture

```
User (Text / Voice)
        ↓
Orchestrator (LangGraph)
        ↓
┌─────────────────────────────┐
│ Planner Agent               │
│ ─ Intent & routing          │
└──────────────┬──────────────┘
               ↓
┌──────────────────────────────────────────┐
│ Execution Agents                          │
│ - Document QA (RAG)                      │
│ - Memory Agent                           │
│ - MCP Tool Agent                         │
│ - Voice Agent                            │
└──────────────┬───────────────────────────┘
               ↓
Groq LLM API (Reasoning Only)
```

---

## 🧩 Project Structure

```
aegismind/
│
├── agents/
│   ├── planner.py        # Intent detection & routing
│   ├── doc_qa.py         # RAG-based document agent
│   ├── memory.py         # Memory read/write logic
│   ├── voice.py          # STT / TTS handling
│   └── mcp_agent.py      # MCP tool integration
│
├── orchestration/
│   ├── graph.py          # LangGraph definition
│   └── state.py          # Global agent state schema
│
├── rag/
│   ├── loader.py         # Document loading
│   ├── embedder.py       # Embedding generation
│   └── retriever.py      # Vector search
│
├── memory/
│   ├── short_term.py     # Session memory
│   └── long_term.db      # Persistent memory store
│
├── services/
│   └── groq_client.py    # Groq API wrapper
│
├── ui/
│   ├── cli.py            # CLI interface
│   └── web.py            # (Optional) Web UI
│
└── main.py               # Entry point
```

---

## 🔁 Agent Execution Flow

1. User sends text or voice input
2. Planner agent classifies intent
3. Orchestrator routes request
4. Relevant agents execute tasks
5. Groq LLM performs reasoning
6. Memory is updated (if needed)
7. Final response returned (text/voice)

---

## 🛠️ Tech Stack

* **LLM Inference:** Groq API (LLaMA 3 / Mixtral)
* **Agent Orchestration:** LangGraph
* **Embeddings:** HuggingFace (CPU-friendly models)
* **Vector Store:** FAISS / Chroma (local)
* **Memory Storage:** SQLite / JSON
* **Voice:** Whisper (STT), Piper / Coqui (TTS)
* **Protocol:** MCP (Model Context Protocol)

---

## 📅 Development Roadmap (10 Days)

* Day 1–2: Core architecture & orchestrator
* Day 3–4: Multi-agent routing
* Day 5–6: Document upload & RAG
* Day 7: Memory system
* Day 8: Memory + agents integration
* Day 9: Voice or MCP integration
* Day 10: Cleanup, README, demo

---

## 🎯 Learning Outcomes

By completing this project, you will understand:

* How real agentic AI systems are structured
* Why planning must be separated from execution
* How to design reliable memory for LLMs
* How to ground LLM responses using RAG
* How to integrate tools via open protocols (MCP)

---

## 📌 Disclaimer

This project prioritizes **learning and architectural correctness** over production scale. It is designed as a **flagship portfolio project** for AI/ML and Agentic AI roles.

---

## 📄 License

MIT License
