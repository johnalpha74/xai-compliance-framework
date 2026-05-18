import os
import requests
import yaml
from urllib.parse import urlparse

RAW_DIR = "data/raw/pdfs"
# CONFIG_PATH = "configs/sources.yaml"
CONFIG_PATH = "configs/extracted_pdf_links.yaml"

os.makedirs(RAW_DIR, exist_ok=True)

def safe_filename(name: str) -> str:
    return name.lower().replace(" ", "_").replace("/", "_") + ".pdf"


def download_pdf(url: str, filename: str):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        if "pdf" not in response.headers.get("Content-Type", "").lower():
            print(f"Skipped, not a PDF: {url}")
            return

        path = os.path.join(RAW_DIR, filename)

        with open(path, "wb") as file:
            file.write(response.content)

        print(f"Downloaded: {path}")

    except Exception as error:
        print(f"Failed to download: {url}")
        print(f"Reason: {error}")


def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    for source in config["sources"]:
        if source.get("type") == "pdf":
            filename = safe_filename(source["name"])
            download_pdf(source["url"], filename)


if __name__ == "__main__":
    main()