# Echo Bot

Echo Bot is a private, cross-platform, local-first career assistant. It is the
desktop shell that brings together:

- **Echo Profile**: your private professional knowledge base and authoritative
  source of verified career facts.
- **Echo Resume**: an evidence-constrained tailored LaTeX resume generator.
- **Echo Chat**: an AI version of you for private resume and career questions.

The application uses Python 3.11, PySide6, SQLite, LanceDB, locally installed
Ollama models, and local LaTeX tooling.

The legacy Streamlit/OpenSearch document-chat application remains temporarily
while the desktop replacement is implemented. Do not use it as the architecture
for new features.

See:

- [`docs/PROJECT.md`](docs/PROJECT.md) for the product and privacy contract.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for module boundaries.
- [`docs/MIGRATION.md`](docs/MIGRATION.md) for migration status.
- [`AGENTS.md`](AGENTS.md) for repository implementation guidance.

After installing the declared dependencies locally:

```bash
python -m scripts.check_offline_readiness
python -m app.main
```

The readiness command only inspects local dependencies, local executables, and
the explicitly configured loopback Ollama service. It never downloads models.

## Legacy Application

# Build Your Local RAG System with LLMs

Welcome to the **Local LLM-based Retrieval-Augmented Generation (RAG) System**! This repository provides the full code to build a private, offline RAG system for managing and querying personal documents locally using a combination of OpenSearch, Sentence Transformers, and Large Language Models (LLMs). Perfect for anyone seeking a privacy-friendly solution to manage documents without relying on cloud services.

![Demo Image](images/chatbot.png)

### 🌟 Key Features:
- **Privacy-Friendly Document Search:** Search through personal documents without uploading them to the cloud.
- **Hybrid Search with OpenSearch:** Uses both traditional text matching and semantic search.
- **Easy Integration with LLMs**: Leverage local LLMs for personalized, context-aware responses.

### 🚀 Get Started
1. Clone the repo: `git clone https://github.com/JAMwithAI/build_your_local_RAG_system.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `constants.py` for embedding models and OpenSearch settings.
4. Run the Streamlit app: `streamlit run welcome.py`

### 📘 Blog Guide
For a detailed walkthrough of the setup and code, check out our blog:

[**Build a Local LLM-based RAG System for Your Personal Documents - Part 1**](https://jamwithai.substack.com/p/build-a-local-llm-based-rag-system)

[**Build a Local LLM-based RAG System for Your Personal Documents - Part 2: The Guide**](https://jamwithai.substack.com/p/build-a-local-llm-based-rag-system-628)

---

Enjoy your journey in building a private, AI-driven document management system! If you find this project useful, consider sharing it with others in the community!
