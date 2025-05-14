import os
import pdfplumber

PDF_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "The_Technical_Debt_Dataset.pdf")

def extract_metrics():
    metrics = {}
    with pdfplumber.open(PDF_PATH) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            lines = text.split("\n")
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 9:
                    try:
                        numeric_values = []
                        name_parts = []
                        for part in parts:
                            try:
                                value = int(part.replace(",", ""))
                                numeric_values.append(value)
                            except ValueError:
                                if numeric_values:
                                    break
                                name_parts.append(part)

                        name = " ".join(name_parts).strip()
                        if len(numeric_values) >= 6:
                            metrics[name] = {
                                "refactorings": numeric_values[3],
                                "code_smells": numeric_values[4],
                                "faults": numeric_values[5]
                            }
                    except Exception as e:
                        print(f"⚠️ Failed to parse line: '{line}' - {e}")
    return metrics

def extract_raw_text_lines():
    print("\n Debugging PDF Text Extraction:\n")
    with pdfplumber.open(PDF_PATH) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(f"\n📄 Page {page_num + 1}:")
            print(page.extract_text())

if __name__ == "__main__":
    print("Testing metric extraction...\n")
    result = extract_metrics()
    print("\nExtracted Metrics:")
    for project, data in result.items():
        print(f"{project}: {data}")