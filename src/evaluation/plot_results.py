import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_FILE = Path("outputs/evaluation_results.csv")
CHART_DIR = Path("outputs/charts")

CHART_DIR.mkdir(parents=True, exist_ok=True)


def save_bar_chart(data, title, xlabel, ylabel, filename):
    plt.figure(figsize=(8, 5))
    data.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(CHART_DIR / filename, dpi=300)
    plt.close()


def generate_charts():
    df = pd.read_csv(RESULTS_FILE)

    # Accuracy by category
    accuracy_by_category = df.groupby("Expected_Category")["Accuracy_Match"].mean()
    save_bar_chart(
        accuracy_by_category,
        "Accuracy by Regulatory Category",
        "Regulatory Category",
        "Accuracy",
        "accuracy_by_category.png"
    )

    # Hallucination rate by category
    hallucination_by_category = df.groupby("Expected_Category")["Hallucination_Flag"].mean()
    save_bar_chart(
        hallucination_by_category,
        "Hallucination Rate by Regulatory Category",
        "Regulatory Category",
        "Hallucination Rate",
        "hallucination_by_category.png"
    )

    # Average latency by category
    latency_by_category = df.groupby("Expected_Category")["Latency_Seconds"].mean()
    save_bar_chart(
        latency_by_category,
        "Average Latency by Regulatory Category",
        "Regulatory Category",
        "Latency Seconds",
        "latency_by_category.png"
    )

    # Explainability metrics
    explainability_metrics = pd.Series({
        "Source Attribution": df["Source_Accuracy"].mean(),
        "Explanation Quality": df["Explanation_Quality"].mean(),
        "Audit Trace": df["Audit_Trace_Complete"].mean(),
        "Keyword Coverage": df["Keyword_Coverage"].mean()
    })

    save_bar_chart(
        explainability_metrics,
        "Explainability Evaluation Metrics",
        "Metric",
        "Score",
        "explainability_metrics.png"
    )

    print("Charts generated successfully.")
    print(f"Saved to: {CHART_DIR}")


if __name__ == "__main__":
    generate_charts()