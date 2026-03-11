from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_DB_PATH = "backend/knowledge_base/vector_db"

def search_guidelines(query):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = vector_db.similarity_search(query, k=3)

    print("\nTop relevant guideline chunks:\n")

    for i, doc in enumerate(docs):
        print(f"\n--- Result {i+1} ---\n")
        print(doc.page_content)


if __name__ == "__main__":
    search_guidelines("tuberculosis symptoms red flag")