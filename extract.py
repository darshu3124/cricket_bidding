import fitz  # PyMuPDF
import sys

def extract_text(pdf_path, output_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    pdf_file = r"C:\Users\HP\Downloads\bbhc league.pdf"
    out_file = "d:/cricket/extracted.txt"
    extract_text(pdf_file, out_file)
