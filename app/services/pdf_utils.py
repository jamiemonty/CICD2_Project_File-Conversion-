from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def txt_to_pdf(txt_path: str, pdf_path: str) -> None:

    txt_path = str(txt_path)
    pdf_path = str(pdf_path)

    text = Path(txt_path).read_text(encoding="utf-8", errors="replace").splitlines()

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    x = 40
    y = height - 50
    line_height = 14

    for line in text:
        if y <= 50:
            c.showPage()
            y = height - 50
            
        # if line is too long, split it into chunks
        max_chars = 110
        chunks = [line[i:i+max_chars] for i in range(0, len(line), max_chars)] or [""]

        for chunk in chunks:
            if y <= 50:
                c.showPage()
                y = height - 50
            c.drawString(x, y, chunk)
            y -= line_height

    c.save()
