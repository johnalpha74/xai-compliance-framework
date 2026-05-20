from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.utils.bedrock_client import generate_with_bedrock

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


def retrieve_context(query: str, k: int = 5):
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search(query, k=k)

    context_blocks = []

    for i, doc in enumerate(results, start=1):
        source = doc.metadata.get("source_file", "Unknown source")
        chunk_id = doc.metadata.get("chunk_id", "Unknown chunk")

        context_blocks.append(
            f"[Source {i}: {source}, Chunk {chunk_id}]\n{doc.page_content}"
        )

    return "\n\n".join(context_blocks), results


def generate_basic_response(query: str, context: str):
    """
    Temporary rule-based response.
    Later we will replace this with AWS Bedrock.
    """

    return f"""
Compliance Question:
{query}

Relevant Regulatory Context:
{context[:3000]}

Draft Compliance Response:
Based on the retrieved regulatory context, the compliance response should be grounded in the cited regulatory sources above. The system should identify the applicable obligation, explain the requirement, and indicate whether further human compliance review is required.

Explanation:
The answer is based only on the retrieved regulatory text. This supports traceability and reduces unsupported AI-generated claims.
"""

def generate_compliance_response(query: str, context: str):
    prompt = f"""
You are an AI compliance assistant for financial regulatory monitoring.

Answer the question using ONLY the regulatory context provided.
Do not invent facts.
If the answer is not supported by the context, say that the context is insufficient.

Compliance Question:
{query}

Regulatory Context:
{context[:1200]}

Required Answer Format:
1. Compliance Answer
2. Relevant Regulatory Basis
3. Explanation
4. Human Review Required: Yes/No
"""

    return generate_with_bedrock(prompt)

def main():
    query = input("Enter compliance query: ")

    print("\nRetrieving relevant regulatory context...")
    context, results = retrieve_context(query, k=1)

    print("\nGenerating compliance response...")
    response = generate_compliance_response(query, context)

    print("\n" + "=" * 100)
    print(response)
    print("=" * 100)


if __name__ == "__main__":
    main()