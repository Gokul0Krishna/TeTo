import fpdf2 as pdf


def Create_pdf(content, filename):
    pdf_doc = pdf.FPDF()
    pdf_doc.add_page()
    pdf_doc.set_font("Arial", size=12)
    pdf_doc.multi_cell(0, 10, content)
    pdf_doc.output(filename)
    