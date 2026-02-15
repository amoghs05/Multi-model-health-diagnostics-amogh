# ocr_engine.py
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from pathlib import Path

# -------- SET PATHS ---------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler\Library\bin"
# -----------------------------


def read_pdf_text(pdf_path):
    """Extract text from PDF using pdfplumber, fallback to OCR."""
    pdf_path = Path(pdf_path)
    
    text = ""

    # Try digital PDF extraction
    try:
        with pdfplumber.open(pdf_path) as pdf:
            extracted = []
            for page in pdf.pages:
                extracted.append(page.extract_text() or "")
            text = "\n".join(extracted)
    except:
        text = ""

    # If digital extraction failed or is too small → OCR
    if len(text.strip()) < 40:
        print("⚠ Using OCR fallback...")
        images = convert_from_path(str(pdf_path), dpi=200, poppler_path=POPPLER_PATH)

        ocr_text = []
        for img in images:
            img = img.convert("L")
            text_img = pytesseract.image_to_string(img)
            ocr_text.append(text_img)

        text = "\n".join(ocr_text)

    return text
