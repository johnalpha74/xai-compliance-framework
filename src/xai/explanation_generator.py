# src/xai/explanation_generator.py
# Convert retrieved regulatory sources and LLM responses into explainable compliance decisions.

def generate_explanation(query, retrieved_docs, compliance_answer):
    """
    Generate explainable compliance output.
    """

    explanation = {
        "query": query,
        "retrieved_sources": [],
        "reasoning_steps": [],
        "compliance_decision": compliance_answer
    }

    # Source Attribution
    for doc in retrieved_docs:
        explanation["retrieved_sources"].append(
            doc.metadata.get("source", "Unknown Source")
        )

    # Simple reasoning trace
    explanation["reasoning_steps"] = [
        "Retrieved relevant regulatory documents",
        "Matched query against regulatory requirements",
        "Generated compliance interpretation",
        "Produced compliance decision"
    ]

    return explanation