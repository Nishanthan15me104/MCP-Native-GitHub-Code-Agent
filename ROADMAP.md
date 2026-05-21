# Project Roadmap & Feature Tracker: MCP GitHub Code Agent

This document tracks the architectural phases, active feature implementations, and upcoming backlog items for the MCP-Native GitHub Code Agent.

---

## 1. Core Architectural Phases

### Phase 1: Environment & GitHub GraphQL Setup
*   Initialize Python virtual environment and dependencies (`gql`, `requests`, `pydantic`).
*   Configure GitHub Personal Access Token (PAT) with repository read permissions.
*   Build and test raw GraphQL queries to fetch repo file trees and file contents.

### Phase 2: Build the GitHub MCP Server
*   Implement the Model Context Protocol (MCP) framework in Python.
*   Expose GraphQL collection logic as standardized MCP tools (`get_repo_structure`, `read_file_content`).
*   Verify tool-discovery compliance using an MCP inspector or direct client calls.

### Phase 3: Hybrid Vector DB Ingestion (RAG)
*   Set up a local or cloud vector database (e.g., Qdrant or Pinecone).
*   Implement a code-aware semantic chunking script (parsing by functions/classes where possible).
*   Generate dense embeddings and write chunks to the DB with strict file-path metadata.

### Phase 4: Build the Agentic Router & Context Manager
*   Configure the core LLM orchestration engine (using Groq for low-latency inference).
*   Implement agentic routing: Teach the model when to use the Semantic Vector DB vs. precise MCP GraphQL tools.
*   Build stateful context pruning to trim older retrieved text blocks and prevent token window overflows.

### Phase 5: UI & Deterministic Evaluation
*   Build a responsive Streamlit or FastAPI web frontend.
*   Enforce structural determinism: Set temperature to `0.0` and enforce rigid validation boundaries.
*   Add evaluation logging to verify answer groundedness against the source codebase.

---

## 2. Feature Implementation Tracker

| Phase | Feature Description | Status | Target Completion | Notes / Blockers |
| :--- | :--- | :--- | :--- | :--- |
| Phase 1 | GraphQL Repository Tree Query | ⬜ Planned | | Must fetch full file path arrays in a single call |
| Phase 1 | File Content Fetcher | ⬜ Planned | | Read raw text/blob via GraphQL node ID |
| Phase 2 | Core MCP Protocol Integration | ⬜ Planned | | Wrap queries into schema-compliant tools |
| Phase 3 | Code Ingestion Pipeline | ⬜ Planned | | Exclude binary files, `.git`, and lockfiles |
| Phase 3 | Vector Database Connection | ⬜ Planned | | Set up local instance or free-tier cloud cluster |
| Phase 4 | Agent Router Logic | ⬜ Planned | | System prompts to distinguish global vs local queries |
| Phase 4 | History Pruning Layer | ⬜ Planned | | Evict old context chunks while keeping chat text |
| Phase 5 | Frontend User Interface | ⬜ Planned | | Simple input/output log with source citations |
| Phase 5 | Groundedness Validator | ⬜ Planned | | Check output facts against retrieved code snippets |

> *Status options: ⬜ Planned | 🟨 In Progress | ✅ Completed | ❌ Blocked*

---

## 3. Dynamic Feature Backlog
*Use this section to drop new ideas, interview-inspired modifications, or feature upgrades as you build.*

*   **[Example Idea] Semantic Cache Layer:** Cache semantically identical user queries to save Groq token costs and lower latency.
*   **[Add New Features Here]:**