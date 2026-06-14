def keyword_coverage(answer, keywords):
    answer = str(answer).lower()
    raw_keywords = str(keywords).replace(";", ",").replace("|", ",")

    keyword_list = [
        k.strip().lower()
        for k in raw_keywords.split(",")
        if k.strip()
    ]

    if not keyword_list:
        return 0

    matched = sum(1 for k in keyword_list if k in answer)

    return round(matched / len(keyword_list), 2)


def source_accuracy(expected_source, retrieved_sources):
    expected_source = str(expected_source).lower()

    retrieved_text = " ".join(
        str(src.get("source_file", "")).lower()
        for src in retrieved_sources
    )

    expected_source = (
        expected_source
        .replace("section", "")
        .replace("recommendation", "")
        .replace("-", " ")
        .replace("_", " ")
    )

    expected_terms = [
        term.strip()
        for term in expected_source.split()
        if len(term.strip()) > 2
    ]

    if not expected_terms:
        return 0

    matches = sum(1 for term in expected_terms if term in retrieved_text)

    return 1 if matches >= 1 else 0


def explanation_quality(reasoning_trace):
    return 1 if len(reasoning_trace) >= 6 else 0