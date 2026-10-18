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
def findandcreatefolder(search_query: str) -> str:
    """Searches for folders matching or partially matching the query inside ~/Desktop/temp/college.
    If no match is found, creates the folder path.

    Args:
        search_query: The folder name or partial path to look for (e.g., "test" or "semester1/assignments").
    """
    # Resolve absolute path for ~/Desktop/temp/college
    base_dir = Path.expanduser(Path("~/Desktop/temp/College"))
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Search recursively for directories matching the query pattern
    matches = [str(p) for p in base_dir.rglob(f"*{search_query}*") if p.is_dir()]
    
    if matches:
        msg = f"Found matching folders:\n" + "\n".join(matches)
        print(msg)
        return msg
    else:
        # If no match exists, create the target directory inside the base path
        target_path = base_dir / search_query
        target_path.mkdir(parents=True, exist_ok=True)
        msg = f"No match found. Created folder at: {target_path.resolve()}"
        print(msg)
        return msg


if __name__ == "__main__":
    findandcreatefolder("test")