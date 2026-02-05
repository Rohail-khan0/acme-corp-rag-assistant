import os
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# 1. .env file load karein
load_dotenv()

# 2. Key ko sahi tariqe se variable mein store karein (quotes lazmi hain)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@st.cache_resource(show_spinner=False)
def initialize_rag_system():
    """
    Initializes the RAG system: loads data, creates embeddings, builds vector store,
    sets up the retriever and LLM.
    """
    try:
        # 1. Load Data
        base_dir = os.path.dirname(os.path.abspath(__file__))
        text_path = os.path.join(base_dir, "Company_sample.txt")
        excel_path = os.path.join(base_dir, "company_data.xlsx")

        if not os.path.exists(text_path) or not os.path.exists(excel_path):
             raise FileNotFoundError("Data files (Company_sample.txt, company_data.xlsx) not found.")

        loader_text = TextLoader(text_path)
        loader_excel = UnstructuredExcelLoader(excel_path)
        
        docs = loader_text.load() + loader_excel.load()

        # 2. Split Text
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        # 3. Embeddings (Yahan variable sahi kar diya gaya hai)
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key = GOOGLE_API_KEY
        )

        # 4. Vector Store
        vectorstore = FAISS.from_documents(chunks, embeddings)

        # 5. Retriever
        retriever = vectorstore.as_retriever(search_type="similarity", k=3)

        # 6. Prompt Template
        prompt_template = PromptTemplate(
            input_variables=["context", "question"], # Fixed: Use list [] instead of set {}
            template="""You are a helpful assistant that answers questions based on the provided context.

            Context: {context}
            Question: {question}

            Answer: Provide a clear and concise answer based on the context above, if the context doesn't contain enough information to answer the answer then say so"""
        )

        # 7. LLM (Yahan bhi variable fix kar diya gaya hai)
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.5
        )

        return {
            "retriever": retriever,
            "prompt_template": prompt_template,
            "llm": llm
        }
    except Exception as e:
        raise RuntimeError(f"Failed to initialize RAG system: {str(e)}")

def get_rag_response(query, components):
    """
    Processes a query using the RAG components.
    """
    retriever = components["retriever"]
    prompt_template = components["prompt_template"]
    llm = components["llm"]

    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = prompt_template.format(context=context, question=query)
    response = llm.invoke(prompt)
    return response.content