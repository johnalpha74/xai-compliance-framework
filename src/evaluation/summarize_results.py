import pandas as pd
from pathlib import Path
from src.evaluation.classification_metrics import compute_classification_metrics

RESULTS_FILE = Path("outputs/evaluation_results.csv")
SUMMARY_FILE = Path("outputs/evaluation_summary.csv")


def summarize_results():

    df = pd.read_csv(RESULTS_FILE)

    # Classification metrics
    y_true = [1] * len(df)
    y_pred = df["Accuracy_Match"].tolist()

    precision, recall, f1 = compute_classification_metrics(
        y_true,
        y_pred
    )

    summary = {

        "Total_Scenarios": len(df),

        "Accuracy": round(
            df["Accuracy_Match"].mean(), 2
        ),

        "Precision": round(
            precision, 2
        ),

        "Recall": round(
            recall, 2
        ),

        "F1_Score": round(
            f1, 2
        ),

        "Hallucination_Rate": round(
            df["Hallucination_Flag"].mean(), 2
        ),

        "Average_Latency_Seconds": round(
            df["Latency_Seconds"].mean(), 2
        ),

        "Minimum_Latency_Seconds": round(
            df["Latency_Seconds"].min(), 2
        ),

        "Maximum_Latency_Seconds": round(
            df["Latency_Seconds"].max(), 2
        ),

        "Keyword_Coverage": round(
            df["Keyword_Coverage"].mean(), 2
        ),

        "Source_Attribution_Accuracy": round(
            df["Source_Accuracy"].mean(), 2
        ),

        "Explanation_Quality": round(
            df["Explanation_Quality"].mean(), 2
        ),

        "Audit_Trace_Completeness": round(
            df["Audit_Trace_Complete"].mean(), 2
        )
    }

    summary_df = pd.DataFrame([summary])

    summary_df.to_csv(
        SUMMARY_FILE,
        index=False
    )

    print("\nEvaluation Summary")
    print("=" * 50)

    for key, value in summary.items():
        print(f"{key}: {value}")

    print(f"\nSaved summary to: {SUMMARY_FILE}")


if __name__ == "__main__":
    summarize_results()