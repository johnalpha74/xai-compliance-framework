from pathlib import Path
import json

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

TEXT_DIR = Path("data/processed/text")
VECTORSTORE_DIR = Path("data/vectorstore/faiss_index")
METADATA_FILE = Path("data/vectorstore/chunk_metadata.json")

VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_text_documents():
    documents = []

    for text_file in TEXT_DIR.glob("*.txt"):
        loader = TextLoader(str(text_file), encoding="utf-8")
        loaded_docs = loader.load()

        for doc in loaded_docs:
            doc.metadata["source_file"] = text_file.name
            documents.append(doc)

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    return chunks


def build_faiss_index(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(str(VECTORSTORE_DIR))

    return vectorstore


def save_chunk_metadata(chunks):
    metadata = []

    for chunk in chunks:
        metadata.append({
            "chunk_id": chunk.metadata.get("chunk_id"),
            "source_file": chunk.metadata.get("source_file"),
            "preview": chunk.page_content[:300]
        })

    with open(METADATA_FILE, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)


def main():
    print("Loading extracted text documents...")
    documents = load_text_documents()

    if not documents:
        print("No text documents found in data/processed/text")
        return

    print(f"Loaded {len(documents)} documents")

    print("Splitting documents into chunks...")
    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    print("Building FAISS vector store...")
    build_faiss_index(chunks)

    print("Saving chunk metadata...")
    save_chunk_metadata(chunks)

    print("FAISS vector store created successfully")
    print(f"Saved to: {VECTORSTORE_DIR}")


if __name__ == "__main__":
    main()