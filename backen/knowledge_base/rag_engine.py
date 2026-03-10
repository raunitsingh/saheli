import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


DOCS_PATH = "backend/knowledge_base/docs"


def build_vector_db():

    documents = []

    for file in os.listdir(DOCS_PATH):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DOCS_PATH, file))
            docs = loader.load()
            documents.extend(docs)

    print(f"Loaded {len(documents)} pages")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_documents(chunks, embeddings)

    vector_db.save_local("backend/knowledge_base/vector_db")

    print("Vector database built successfully")


if __name__ == "__main__":
    build_vector_db()