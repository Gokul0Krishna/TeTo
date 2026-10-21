import os
from pathlib import Path
import fpdf as pdf


def Create_pdf(content: str, filename: str) -> None:
    """Creates a PDF file with the given content and saves it to the specified filename.
    """
    pdf_doc = pdf.FPDF()
    pdf_doc.add_page()
    pdf_doc.set_font("Arial", size=12)
    pdf_doc.multi_cell(0, 10, content)
    pdf_doc.output(filename)


def list_college_folders() -> list[str]:
    """List all available folder paths under ~/Desktop/temp/College."""
    base_dir = os.path.expanduser("~/Desktop/temp/College")
    
    # Ensure the base directory exists so os.walk doesn't fail
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
        return [base_dir]
    
    folder_paths = []
    for root, dirs, _ in os.walk(base_dir):
        for d in dirs:
            folder_paths.append(os.path.join(root, d))
            
    return folder_paths


if __name__ == "__main__":
    findandcreatefolder("Test")