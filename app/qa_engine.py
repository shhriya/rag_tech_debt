# import os
# import pdfplumber
# from dotenv import load_dotenv
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# from langchain_community.vectorstores import Chroma
# from langchain.chains import RetrievalQA

# load_dotenv()

# PDF_PATH = os.path.join(
#     os.path.dirname(os.path.dirname(__file__)), "data", "The_Technical_Debt_Dataset.pdf"
# )
# CHROMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vectorstore")


# def load_pdf_text(path):
#     text_chunks = []
#     print("Loading PDF from:", path)
#     with pdfplumber.open(path) as pdf:
#         for i, page in enumerate(pdf.pages):
#             text = page.extract_text()
#             if text:
#                 print(f"Page {i + 1} text length: {len(text)}")
#                 text_chunks.append(text)
#             else:
#                 print(f"No text found on page {i + 1}")
#     return "\n".join(text_chunks)


# def get_or_create_vectorstore():
#     print(" Rebuilding vectorstore from scratch...")

#     raw_text = load_pdf_text(PDF_PATH)
#     if not raw_text.strip():
#         raise ValueError("PDF text is empty! Nothing to embed.")

#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=250)
#     docs = splitter.create_documents([raw_text])
#     print(f" Loaded {len(docs)} chunks")

#     embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#     vectordb = Chroma.from_documents(
#         docs, embedding_model, persist_directory=CHROMA_DIR
#     )
#     vectordb.persist()
#     return vectordb


# def get_qa_chain():
#     retriever = get_or_create_vectorstore().as_retriever()
#     llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
#     return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


# class TechDebtQnA:
#     def __init__(self):
#         self.chain = get_qa_chain()

#     def answer_question(self, question: str) -> str:
#         return self.chain.invoke({"query": question})

import os
import pdfplumber
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

load_dotenv()

PDF_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "The_Technical_Debt_Dataset.pdf"
)
CHROMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vectorstore")


def load_pdf_text(path):
    text_chunks = []
    print("📄 Loading PDF from:", path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF not found at {path}")

    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                print(f"📄 Page {i + 1} text length: {len(text)}")
                text_chunks.append(text)
            else:
                print(f"⚠️ No text found on page {i + 1}")
    return "\n".join(text_chunks)


def get_or_create_vectorstore():
    print("🔁 Rebuilding vectorstore from scratch...")

    raw_text = load_pdf_text(PDF_PATH)
    if not raw_text.strip():
        raise ValueError("❌ PDF text is empty! Nothing to embed.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=250)
    docs = splitter.create_documents([raw_text])
    print(f"✅ Loaded {len(docs)} chunks")

    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = Chroma.from_documents(
        docs, embedding_model, persist_directory=CHROMA_DIR
    )
    vectordb.persist()
    return vectordb


def get_qa_chain():
    retriever = get_or_create_vectorstore().as_retriever()
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


class TechDebtQnA:
    def __init__(self):
        self.chain = get_qa_chain()

    def answer_question(self, question: str) -> str:
        return self.chain.invoke({"query": question})
