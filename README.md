# EDWIN

> **A local-first AI operating system built for everyday computing.**

EDWIN is an intelligent desktop AI designed to run primarily on your own hardware. Instead of being just another chatbot, EDWIN combines local language models, persistent memory, hardware awareness, model management, and a native desktop experience into a unified AI operating system.

The long-term goal is to build an AI that understands its user, remembers over time, manages its own AI models, and performs meaningful work while keeping personal data private whenever possible.

---

## Why EDWIN?

Today's AI assistants are excellent at conversation but poor at becoming true personal assistants.

EDWIN is built around a different philosophy:

* **Local-first** whenever practical
* **Privacy by design**
* **Persistent memory**
* **Native desktop integration**
* **Hardware-aware AI**
* **User ownership of data**

Instead of treating AI as a webpage, EDWIN treats it as software that lives on your computer and grows alongside you.

---

# Features

## Current (v0.1.1)

### AI Backend

* FastAPI-powered local backend
* Modular agent controller
* Local model routing
* Ollama integration
* Memory retrieval pipeline

### Desktop Application

* Native desktop application using Tauri
* React + TypeScript frontend
* Modern chat interface
* Hardware information panel
* Model management interface

### System Management

* Hardware detection
* Runtime detection
* Persistent application state
* State migration framework
* Model recommendation engine
* Model verification
* Local model installer
* Setup service
* Versioned application state

### Memory

* Long-term memory using ChromaDB
* Persistent local storage
* Context retrieval
* Memory routing

---

# Roadmap

## ✅ v0.1.0

Initial Alpha

* Local chat
* Memory system
* Basic desktop application

---

## ✅ v0.1.1

Setup Milestone

* Hardware detection
* Runtime detection
* Setup architecture
* Model management
* Persistent state
* Desktop setup UI

---

## 🔄 v0.2.0

Authentication & Installer

Planned:

* First-run installer
* User authentication
* Licensing
* Automatic updates
* Device registration

---

## Planned Future Releases

### v0.3.0

* Improved long-term memory
* Better context retrieval
* Memory visualization

### v0.4.0

* Autonomous task execution
* Workflow engine
* Background jobs

### v0.5.0

* Plugin ecosystem
* External integrations
* Third-party tools

### v1.0.0

First stable public release.

---

# Architecture

```
                  ┌──────────────────────────┐
                  │   React + Tauri Desktop  │
                  └──────────────┬───────────┘
                                 │
                                 ▼
                    FastAPI Local Backend
                                 │
      ┌──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼
  Agent Core     Memory Engine   System Core   Model Manager
      │              │              │              │
      ▼              ▼              ▼              ▼
 Decision       ChromaDB      Hardware API     Ollama Models
 Engine         Memory         Setup           Installation
```

---

# Repository Structure

```
EDWIN-AI/
│
├── desktop/                # React + Tauri desktop application
│
├── system/                 # Setup and system services
│   ├── app_state.py
│   ├── hardware_detector.py
│   ├── model_catalog.py
│   ├── model_installer.py
│   ├── model_selector.py
│   ├── runtime_detector.py
│   ├── setup_service.py
│   └── ...
│
├── scripts/                # Development scripts
│
├── api.py                  # FastAPI backend
├── agent_controller.py     # AI orchestration
├── memory_bridge.py        # Memory integration
├── memory_manager.py       # Memory management
│
└── requirements.txt
```

---

# Technology Stack

### Backend

* Python
* FastAPI
* ChromaDB
* Ollama

### Frontend

* React
* TypeScript
* Tauri
* Vite

### AI

* Local LLMs
* Embeddings
* Retrieval-Augmented Generation (RAG)

---

# Installation

## Prerequisites

* Python 3.10+
* Node.js
* npm
* Rust (for Tauri)
* Ollama

---

## Clone

```bash
git clone https://github.com/maple7876/EDWIN-AI.git

cd EDWIN-AI
```

---

## Backend

```bash
pip install -r requirements.txt

python api.py
```

---

## Desktop

```bash
cd desktop

npm install

npm run tauri dev
```

---

# Development

Useful commands:

### Run frontend

```bash
cd desktop

npm run dev
```

### Lint

```bash
npm run lint
```

### Production build

```bash
npm run build
```

---

# Design Philosophy

EDWIN follows several core principles.

## Local First

Whenever practical, computation should happen on the user's own machine.

---

## Privacy

Personal information belongs to the user.

EDWIN is designed so that memories, conversations, and models can remain local whenever possible.

---

## Modular

Each subsystem has a clearly defined responsibility.

Examples include:

* Agent
* Memory
* Setup
* Models
* Hardware
* Runtime
* Desktop UI

This modular architecture allows new capabilities to be added without rewriting the entire application.

---

## Long-Term Vision

The long-term objective is to build an AI operating system that can:

* Understand the user's environment
* Remember information over long periods
* Manage local AI models automatically
* Execute useful workflows
* Operate securely and privately
* Become a true personal computing companion

---

# Current Status

Current release:

**EDWIN Alpha v0.1.1**

Status:

* Active development
* Local-first architecture
* Native desktop application
* Setup system complete
* Authentication and installer in progress

---

# Contributing

EDWIN is currently under active development.

Bug reports, suggestions, and constructive feedback are always welcome.

As the project matures, contribution guidelines and issue templates will be added.

---

# License

This repository is currently released under the project's chosen license.

(Replace this section once a LICENSE file is added.)

---

# Acknowledgements

Built using:

* FastAPI
* React
* TypeScript
* Tauri
* Ollama
* ChromaDB

---

# Project Vision

> *"The future of personal AI shouldn't live exclusively in the cloud. It should live with the person who uses it."*

EDWIN is an ongoing effort to create an AI that feels less like a website and more like a true operating system companion—one that respects user privacy, understands its environment, and becomes increasingly useful over time.
