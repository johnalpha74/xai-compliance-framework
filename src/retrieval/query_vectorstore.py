from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTORSTORE_DIR = Path("data/vectorstore/faiss_index")


def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )


def search(query: str, k: int = 5):
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search_with_score(query, k=k)

    for i, (doc, score) in enumerate(results, start=1):
        print("\n" + "=" * 80)
        print(f"Result {i}")
        print(f"Score: {score}")
        print(f"Source: {doc.metadata.get('source_file')}")
        print(f"Chunk ID: {doc.metadata.get('chunk_id')}")
        print("-" * 80)
        print(doc.page_content[:1200])


if __name__ == "__main__":
    query = input("Enter compliance query: ")
    search(query)