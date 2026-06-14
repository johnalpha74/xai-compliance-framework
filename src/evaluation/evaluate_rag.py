import time
import pandas as pd
from pathlib import Path

from src.rag.compliance_rag_pipeline import retrieve_context, generate_compliance_response
from src.xai.explanation_generator import generate_explanation
from src.utils.audit_logger import log_audit_event
from src.evaluation.metrics import (
    keyword_coverage,
    source_accuracy,
    explanation_quality
)

DATASET_FILE = Path("data/evaluation/ground_truth.csv")
OUTPUT_FILE = Path("outputs/evaluation_results.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


def simple_text_match(predicted: str, expected: str) -> int:
    predicted = str(predicted).lower()
    expected = str(expected).lower()

    expected_keywords = expected.split()

    if not expected_keywords:
        return 0

    matches = sum(1 for word in expected_keywords if word in predicted)

    return 1 if matches >= max(1, len(expected_keywords) * 0.3) else 0

def detect_hallucination(answer: str, retrieved_context: str) -> int:
    answer = str(answer).lower()
    retrieved_context = str(retrieved_context).lower()

    if "context is insufficient" in answer:
        return 0

    key_terms = [
        "fica", "fatf", "basel", "sarb", "fsca", "popia",
        "customer", "transaction", "report", "identity",
        "risk", "compliance", "due diligence"
    ]

    unsupported_terms = [
        term for term in key_terms
        if term in answer and term not in retrieved_context
    ]

    return 1 if len(unsupported_terms) >= 3 else 0

def evaluate():
    merged = pd.read_csv(DATASET_FILE)

    # Using first 5 while testing; remove/comment this for all 100
    # merged = merged.head(5)

    results = []

    for _, row in merged.iterrows():
        scenario_id = row["Scenario_ID"]
        query = row["Query"]
        expected_answer = row["Expected_Answer"]
        expected_source = row["Expected_Source"]
        expected_category = row["Expected_Category"]
        keywords = row["Key_Compliance_Keywords"]

        print(f"\nEvaluating {scenario_id}: {query}")

        start_time = time.time()

        context, retrieved_docs = retrieve_context(query, k=1)
        response = generate_compliance_response(query, context)

        latency = time.time() - start_time

        explanation = generate_explanation(
            query=query,
            retrieved_docs=retrieved_docs,
            compliance_answer=response
        )

        audit_file = log_audit_event(explanation)

        accuracy_match = simple_text_match(response, expected_answer)
        hallucination_flag = detect_hallucination(response, context)

        source_count = len(explanation.get("retrieved_sources", []))
        trace_count = len(explanation.get("reasoning_trace", []))

        keyword_score = keyword_coverage(response, keywords)

        source_score = source_accuracy(
            expected_source,
            explanation["retrieved_sources"]
        )

        explanation_score = explanation_quality(
            explanation["reasoning_trace"]
        )

        audit_trace_complete = 1 if source_count > 0 and trace_count >= 5 else 0

        results.append({
            "Scenario_ID": scenario_id,
            "Query": query,
            "Expected_Category": expected_category,
            "Expected_Source": expected_source,
            "Expected_Answer": expected_answer,
            "Generated_Answer": response,
            "Key_Compliance_Keywords": keywords,
            "Accuracy_Match": accuracy_match,
            "Hallucination_Flag": hallucination_flag,
            "Keyword_Coverage": keyword_score,
            "Source_Accuracy": source_score,
            "Explanation_Quality": explanation_score,
            "Latency_Seconds": round(latency, 2),
            "Retrieved_Source_Count": source_count,
            "Reasoning_Trace_Count": trace_count,
            "Audit_Trace_Complete": audit_trace_complete,
            "Audit_File": audit_file
        })

    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT_FILE, index=False)

    print("\nEvaluation complete.")
    print(f"Results saved to: {OUTPUT_FILE}")

    print("\nSummary:")
    print(f"Total scenarios: {len(results_df)}")
    print(f"Accuracy proxy: {results_df['Accuracy_Match'].mean():.2f}")
    print(f"Hallucination rate proxy: {results_df['Hallucination_Flag'].mean():.2f}")
    print(f"Average latency: {results_df['Latency_Seconds'].mean():.2f} seconds")
    print(f"Audit trace completeness: {results_df['Audit_Trace_Complete'].mean():.2f}")
    print(f"Source attribution accuracy: {results_df['Source_Accuracy'].mean():.2f}")
    
    print(
    f"Average keyword coverage: "
    f"{results_df['Keyword_Coverage'].mean():.2f}"
)

    print(
    f"Explanation quality: "
    f"{results_df['Explanation_Quality'].mean():.2f}"
)


if __name__ == "__main__":
    evaluate()