# 🤖 Echo Bot – Your AI Resume Concierge

**Echo** is a personalized AI chatbot built as part of my portfolio to demonstrate applied skills in **LangChain**, **LangGraph**, **FastAPI**, **vector-based RAG (Retrieval-Augmented Generation)**, and **LLM integration** using **Gemini** by Google.

> 🐾 The name *Echo* is inspired by my dog, **Eko** — symbolizing both companionship and the idea of a voice that reflects back thoughtful answers.

---

## 🧠 About Echo
Echo is an AI version of me, Rachel — a friendly, informative digital assistant that helps users explore my background, projects, academic history, and more. It leverages a combination of:

- **LangChain agents & LangGraph** for structured conversational flow
- **Google Generative AI (Gemini 2.0)** for natural language responses
- **RAG (Retrieval-Augmented Generation)** with a FAISS vector store
- **FastAPI** backend with a **React + TypeScript** frontend chatbot widget
- **Custom document ingestion** from `.txt` and `.json` sources (resume, GitHub content, project data)

It’s designed to mimic how I would personally answer questions about my experience, acting as an intelligent resume concierge on my website.

---

## 🔥 Live Demo
Coming soon at [rachem.netlify.app](https://rachem.netlify.app)

---

## 🧠 Features

- 💬 Conversational AI trained on real resume and project data
- 🔗 RAG-enabled using FAISS and Google Generative AI
- ✨ Friendly UX with a React + Styled-Components chat UI
- 🤝 Can answer default or user-supplied questions about Rachel's experience
- 🛠️ Hosted with FastAPI backend + vectorstore setup
- 💼 GitHub repo and external links parsed for context

---

## 📁 Project Structure
```bash
    echo-bot/ 
        ├── main.py # FastAPI app w/ LangGraph and Gemini 
        ├── fetch_github_repo.py # Fetching data from github repository
        ├── generate_vectorstore.py # Generating vectorstore for retrieval documents
        ├── vector_store/ # FAISS vectorstore (RAG base) 
        │   ├── index.faiss
        │   ├── index.pkl
        ├── documents/ # JSON + TXT files (resume, project data) 
        │   └── ... 
        ├── .env 
        └── README.md
```


## 🧰 Tech Stack

| Tech             | Purpose                              |
|------------------|--------------------------------------|
| **FastAPI**       | Backend API for bot communication   |
| **LangGraph**     | Conversational flow control         |
| **Gemini 2.0**    | LLM for response generation         |
| **FAISS**         | Vectorstore for resume/project data |
| **React + TS**    | Frontend chatbot UI                 |
| **Styled Components** | Chat styling + popup animation |
| **Vercel / Railway** | Deployment (Frontend / Backend)  |

---

## 🛠️ Setup Instructions

### Backend

1. Clone the repo and install Python dependencies:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

2. Create .env file:
    ```
    GOOGLE_API_KEY=your_google_api_key
    ```

3. Run FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

---

## 📦 Deployment
- Frontend: Deployed on Netlify.
- Backend: Deployed on Railway.

---

## 🚫 Usage & Licensing

⚠️ **Note:** This project is intended strictly for **portfolio and demonstration purposes**.  
Please do **not reuse, redistribute, or fork** this repository without my express permission.

---

## 👩‍💻 Developed By

Rachem [Portfolio Website](https://rachem.netlify.app) | [LinkedIn](https://www.linkedin.com/in/rachemoniq/)
