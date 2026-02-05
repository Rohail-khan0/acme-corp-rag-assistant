# Acme Corporation RAG Chatbot 🏢 🤖

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-v0.1-green)
![Gemini](https://img.shields.io/badge/Google%20AI-Gemini-orange)

An internal knowledge-base chatbot built for Acme Corporation. This application allows employees to query internal documents using natural language. It utilizes **Retrieval Augmented Generation (RAG)** to provide accurate, context-aware answers sourced directly from Acme's data.



## 🛠 Tech Stack

This project implements a complete RAG pipeline:

* **Document Loader:** Parses PDF/Text documents from the `/data` directory.
* **Text Splitter:** `RecursiveCharacterTextSplitter` for chunking data.
* **Embeddings:** Google Generative AI Embeddings.
* **Vector Store:** **FAISS** (Facebook AI Similarity Search) for local, efficient similarity search.
* **Retriever:** Fetches relevant context chunks based on user query.
* **LLM Generator:** **Google Gemini Pro** (via API).
* **Chain:** LangChain `RetrievalQA` chain.

## 🚀 Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/acme-corp-rag-assistant.git](https://github.com/yourusername/acme-corp-rag-assistant.git)
    cd acme-corp-rag-assistant
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install langchain langchain-google-genai faiss-cpu python-dotenv
    ```

4.  **Environment Variables:**
    Create a `.env` file in the root directory and add your Google API key:
    ```env
    GOOGLE_API_KEY=your_actual_api_key_here
    ```

## 📖 Usage

1.  Place your Acme Corporation documents (PDF, TXT) in the `data/` folder.
2.  Run the chatbot script:
    ```bash
    python main.py
    ```
3.  Enter your question when prompted.

## 📁 Project Structure

```text
acme-corp-rag-assistant/
├── data/               # Store your source documents here
├── vector_store/       # Persisted FAISS index (generated after first run)
├── main.py             # Main application logic
├── .env                # API Keys (gitignored)
└── README.md           # Documentation
