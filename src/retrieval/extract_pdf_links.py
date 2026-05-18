import os
import requests
import yaml
from bs4 import BeautifulSoup
from urllib.parse import urljoin

CONFIG_PATH = "configs/sources.yaml"
OUTPUT_PATH = "configs/extracted_pdf_links.yaml"

HEADERS = {
    "User-Agent": "Mozilla/5.0 academic-research-prototype"
}


def extract_pdf_links(page_url: str):
    response = requests.get(page_url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        full_url = urljoin(page_url, href)

        if ".pdf" in full_url.lower():
            pdf_links.append({
                "title": link.get_text(strip=True) or "Untitled PDF",
                "url": full_url
            })

    return pdf_links


def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    results = {"sources": []}

    for source in config["sources"]:
        if source.get("type") in ["html", "html_index", "html_with_pdf"]:
            print(f"Checking: {source['name']}")
            try:
                pdfs = extract_pdf_links(source["url"])

                for pdf in pdfs:
                    results["sources"].append({
                        "name": pdf["title"],
                        "type": "pdf",
                        "url": pdf["url"],
                        "category": source.get("category"),
                        "source": source.get("source"),
                        "description": source.get("description")
                    })

                print(f"Found {len(pdfs)} PDFs")

            except Exception as error:
                print(f"Failed: {source['url']} - {error}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        yaml.dump(results, file, sort_keys=False, allow_unicode=True)

    print(f"Saved extracted PDF links to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()