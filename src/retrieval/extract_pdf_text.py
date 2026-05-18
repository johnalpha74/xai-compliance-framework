import os
from pathlib import Path
from pypdf import PdfReader

PDF_DIR = Path("data/raw/pdfs")
OUTPUT_DIR = Path("data/processed/text")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())


def extract_text_from_pdf(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        cleaned = clean_text(text)

        if cleaned:
            pages_text.append(f"\n\n--- Page {page_number} ---\n{cleaned}")

    return "\n".join(pages_text)


def main():
    pdf_files = list(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in data/raw/pdfs")
        return

    for pdf_path in pdf_files:
        try:
            print(f"Extracting: {pdf_path.name}")
            text = extract_text_from_pdf(pdf_path)

            output_file = OUTPUT_DIR / f"{pdf_path.stem}.txt"

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Saved: {output_file}")

        except Exception as error:
            print(f"Failed to process {pdf_path.name}")
            print(f"Reason: {error}")


if __name__ == "__main__":
    main()