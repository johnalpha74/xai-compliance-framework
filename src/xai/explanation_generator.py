from pathlib import Path
from datetime import datetime


def generate_explanation(query, retrieved_docs, compliance_answer):
    retrieved_sources = []

    for doc in retrieved_docs:
        source = doc.metadata.get("source_file", "Unknown source")
        chunk_id = doc.metadata.get("chunk_id", "Unknown chunk")

        retrieved_sources.append({
            "source_file": source,
            "chunk_id": chunk_id,
            "preview": doc.page_content[:300]
        })

    if retrieved_sources:
        first_source = Path(retrieved_sources[0]["source_file"]).stem
        first_chunk = retrieved_sources[0]["chunk_id"]
    else:
        first_source = "Unknown regulatory source"
        first_chunk = "Unknown chunk"

    structured_reasoning_trace = [
        {
            "step": 1,
            "stage": "Query Received",
            "description": f"The system received the compliance query: '{query}'."
        },
        {
            "step": 2,
            "stage": "Regulatory Retrieval",
            "description": f"The retrieval layer searched the FAISS vector store and identified relevant regulatory content from {first_source}, chunk {first_chunk}."
        },
        {
            "step": 3,
            "stage": "Source Grounding",
            "description": "The retrieved regulatory text was used as the grounding context for the compliance response."
        },
        {
            "step": 4,
            "stage": "Compliance Interpretation",
            "description": "The system interpreted the retrieved regulatory content in relation to the user query."
        },
        {
            "step": 5,
            "stage": "Compliance Decision Generation",
            "description": "A compliance response was generated based only on the retrieved regulatory context."
        },
        {
            "step": 6,
            "stage": "Human Review Recommendation",
            "description": "Human review is recommended because regulatory compliance decisions require professional validation."
        }
    ]

    explanation = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "retrieved_sources": retrieved_sources,
        "reasoning_trace": structured_reasoning_trace,
        "compliance_decision": compliance_answer
    }

    return explanation