# 🧠 AegisMind

**AegisMind** is a modular, multi-agent AI system built to demonstrate real-world **agentic AI architecture** — orchestration, retrieval-augmented generation, persistent memory, external tool use via the Model Context Protocol (MCP), and voice interaction. It runs fully containerized with Docker and uses free, open, and locally-run components wherever possible.

> Built as a hands-on learning project to understand how production agentic AI systems are actually designed — not just prompt engineering, but the system architecture around it: routing, memory, retrieval, and tool orchestration.

---

## 🎥 Demo

<!-- Add a screenshot or terminal recording GIF here, e.g.: -->
<!-- ![AegisMind Demo](docs/demo.gif) -->

```
You: What agents does AegisMind have?

🧠 PLANNER AGENT
   Intent='document question', Route=AgentType.DOC_QA

📄 DOCUMENT Q&A AGENT
AegisMind: AegisMind has several agents: Planner Agent, Document Q&A 
Agent, Memory Agent, General Agent, and MCP Tool Agent...
```

---

## 🚀 What It Does

AegisMind takes a user message, classifies its intent, and routes it to the right specialized agent:

| Agent | Capability |
|---|---|
| **Planner** | Classifies user intent and routes to the correct agent |
| **General** | Natural conversation via Groq LLM |
| **Document Q&A** | Answers questions using uploaded PDFs/DOCX/TXT (RAG pipeline) |
| **Memory** | Stores and recalls persistent facts about the user (SQLite) |
| **MCP Tool** | Calls external tools (web search, calculator, current time) via the real Model Context Protocol |
| **Voice** | Optional text-to-speech output (Whisper + gTTS) |

---

## 🏗️ Architecture

```
                         User Input
                             ↓
                    ┌────────────────┐
                    │  Planner Agent │  ← classifies intent (Groq LLM)
                    └───────┬────────┘
                            ↓
        ┌───────────┬───────┴───────┬───────────────┐
        ↓            ↓                ↓               ↓
┌───────────────┐ ┌──────────┐  ┌──────────────┐ ┌──────────────┐
│ General Agent │ │  Memory  │  │   Doc Q&A    │ │  MCP Tool    │
│  (Groq chat)  │ │  Agent   │  │ Agent (RAG)  │ │   Agent      │
└───────────────┘ └────┬─────┘  └──────┬───────┘ └──────┬───────┘
                        ↓                ↓                ↓
                 ┌─────────────┐  ┌─────────────┐  ┌──────────────┐
                 │   SQLite    │  │ Loader →    │  │ MCP Client → │
                 │ (long-term  │  │ Embedder →  │  │ tools_server │
                 │   facts)    │  │ FAISS store │  │ (stdio)      │
                 └─────────────┘  └─────────────┘  └──────────────┘

     Short-term conversational memory: Redis (with TTL expiration)
     All agents orchestrated via LangGraph state machine
     LLM inference: Groq (fast, free-tier friendly)
     Entire stack runs in Docker (docker-compose: app + redis)
```

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|---|---|---|
| **Orchestration** | LangGraph | State machine for agent routing and execution |
| **LLM Inference** | Groq API | Extremely fast inference, generous free tier |
| **Document Loading** | LangChain (`langchain-community`) | PDF/DOCX/TXT parsing and chunking |
| **Embeddings** | Sentence Transformers | Free, local, CPU-friendly semantic embeddings |
| **Vector Search** | FAISS | Fast local similarity search, no external service |
| **Long-term Memory** | SQLite | Lightweight, persistent, zero-config |
| **Short-term Memory** | Redis | Shared, fast, TTL-based conversation buffer |
| **Tool Use** | MCP (Model Context Protocol) | Standardized client-server tool integration |
| **Web Search** | DuckDuckGo (`duckduckgo-search`) | Free, no API key required |
| **Speech-to-Text** | OpenAI Whisper (local) | Free, runs offline, no API calls |
| **Text-to-Speech** | gTTS | Free, no API key |
| **Containerization** | Docker + Docker Compose | Reproducible environment across machines |

**Notable design choice:** Every component was deliberately chosen to be **free and either local or generously free-tiered** — no paid APIs required to run this project end-to-end.

---

## 📁 Project Structure

```
aegismind/
├── agents/
│   ├── planner.py         # Intent detection & routing
│   ├── doc_qa.py          # RAG-based document Q&A agent
│   ├── memory.py          # Long-term fact storage/retrieval agent
│   ├── mcp_agent.py       # MCP client — connects to tools_server.py
│   └── voice.py           # Whisper STT + gTTS TTS
│
├── orchestration/
│   ├── graph.py           # LangGraph workflow definition
│   └── state.py           # Shared agent state schema
│
├── rag/
│   ├── loader.py          # Document loading & chunking
│   ├── embedder.py        # Sentence Transformer embeddings
│   └── retriever.py       # FAISS vector store
│
├── memory/
│   ├── long_term.py       # SQLite persistent facts
│   ├── short_term.py      # In-process rolling buffer (legacy/reference)
│   └── redis_short_term.py # Redis-backed short-term memory (active)
│
├── mcp_servers/
│   └── tools_server.py    # Real MCP server: web_search, calculator, current_time
│
├── services/
│   └── groq_client.py     # Groq API wrapper
│
├── config/
│   └── settings.py        # Environment-based configuration (pydantic-settings)
│
├── ui/
│   └── cli.py             # Interactive terminal interface
│
├── data/                   # Documents, embeddings, memory.db (gitignored)
├── Dockerfile
├── docker-compose.yml      # aegismind + redis services
├── requirements.txt
├── .env.example
└── main.py                 # Entry point
```

---

## ⚡ Quick Start

### Prerequisites
- Docker Desktop installed
- A free [Groq API key](https://console.groq.com)

### 1. Clone and Configure

```bash
git clone https://github.com/nishchalacharya/AegisMind-MultiAgentic-Chatbot.git
cd AegisMind-MultiAgentic-Chatbot/aegismind

cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 2. Build and Start

```bash
docker-compose up -d --build
```

This starts two containers: the AegisMind app and a Redis instance for short-term memory.

### 3. Enter the Container and Run

```bash
docker-compose exec aegismind bash
python main.py
```

**With voice output enabled:**
```bash
python main.py --voice
```

### 4. Try It Out

```
You: Hello! How are you?
You: Remember that I live in Kathmandu
You: Where do I live?
You: What is 25 times 8?
You: Search the web for the latest AI news
```

---

## 🧩 Key Design Decisions

**Why LangGraph for orchestration?**
Explicit state management and conditional routing make agent decision-making transparent and debuggable — every step of the Planner's routing logic is inspectable.

**Why SQLite for long-term memory but Redis for short-term?**
Long-term facts (name, location, preferences) need to persist indefinitely — SQLite's file-based durability fits naturally. Short-term conversational context is inherently temporary and benefits from Redis's built-in TTL expiration, plus Redis is architected to scale across multiple processes/workers if this were ever deployed as a multi-user web service.

**Why real MCP instead of custom function-calling?**
Implementing the actual Model Context Protocol (client-server via stdio, JSON-RPC) rather than a simplified custom tool-calling shortcut demonstrates the same integration pattern used by production AI applications like Claude Desktop — tools are discoverable and standardized, not hardcoded.

**Why Docker from the start?**
Cross-machine Python version conflicts (3.11 vs 3.13) during development made a strong case for containerization — the Dockerfile guarantees the exact same environment regardless of host machine.

---

## 🔍 Known Limitations & Honest Trade-offs

- **Live microphone input** was deliberately scoped out — Docker on Windows doesn't cleanly support host audio device passthrough. Voice output (TTS) works; voice input would require running natively or on Linux/Mac with proper audio device mapping.
- **DuckDuckGo web search** can be rate-limited under frequent use; the agent is designed to report this honestly rather than fabricate results when a tool call fails.
- **Guardrails** (PII detection via Presidio, prompt-injection filtering, content-safety classification via Groq's safety models) are architected but not yet implemented — planned as a future enhancement.
- **Redis short-term memory** currently uses a single shared instance; in a true multi-user deployment, this would need proper user-session isolation and authentication.

---

## 🗺️ Roadmap / Possible Extensions

- [ ] Guardrails: regex + Presidio PII detection + Groq safety classifier (input/output filtering)
- [ ] Human-in-the-loop approval via LangGraph's `interrupt()` for sensitive actions
- [ ] LangGraph native checkpointing (`MemorySaver`/`SqliteSaver`) as an alternative to custom memory classes
- [ ] Additional MCP servers (filesystem access, GitHub integration)
- [ ] Web UI (FastAPI + simple frontend) as an alternative to the CLI

---

## 📄 License

MIT License

---

## 🙋 About This Project

Built as a personal learning project to gain hands-on experience with agentic AI system design, LangGraph orchestration, RAG pipelines, the Model Context Protocol, and containerized deployment — with an emphasis on understanding *why* each architectural choice was made, not just implementing it.