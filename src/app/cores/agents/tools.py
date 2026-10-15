import os
from pathlib import Path
from smolagents import tool
import fpdf as pdf


@tool
def Create_pdf(content: str, filename: str) -> None:
    """Creates a PDF file with the given content and saves it to the specified filename.

    Args:
        content: The text content to write inside the PDF file.
        filename: The output path and filename for the saved PDF.
    """
    pdf_doc = pdf.FPDF()
    pdf_doc.add_page()
    pdf_doc.set_font("Arial", size=12)
    pdf_doc.multi_cell(0, 10, content)
    pdf_doc.output(filename)


@tool
def findandcreatefolder(base_path: str, relative_path: str) -> str:
    """Finds a nested folder path; if any part of the path doesn't exist, it creates it.

    Args:
        base_path: The root directory to start from (e.g., "." or "/home/user").
        relative_path: The partial or nested folder path to find/create (e.g., "college/test").
    """
    # Combine the base path and the nested relative path
    target_dir = Path(base_path) / relative_path

    if target_dir.exists() and target_dir.is_dir():
        msg = f"Found existing directory: {target_dir.resolve()}"
        print(msg)
        return msg
    else:
        # Create all intermediate missing directories automatically
        target_dir.mkdir(parents=True, exist_ok=True)
        msg = f"Directory path did not exist. Created: {target_dir.resolve()}"
        print(msg)
        return msg


if __name__ == "__main__":
    # Example usage: handles nested partial paths cleanly
    findandcreatefolder("~/Desktop", "college/test")