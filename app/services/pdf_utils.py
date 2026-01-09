from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def txt_to_pdf(txt_path: str, pdf_path: str) -> None:

    txt_path = str(txt_path)
    pdf_path = str(pdf_path)

    text = Path(txt_path).read_text(encoding="utf-8", errors="replace").splitlines()

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    margin = 50
    x = margin
    y = height - margin
    line_height = 14

    # Calculate usable width for wrapping
    usable_width = width - (margin * 2)

    # Rough chars-per-line estimate 
    ##max_chars = int(usable_width / 5)
    filtered_content = any("*" in line for line in text)

    if filtered_content:
        max_chars = int(usable_width / 5)
    else:
        max_chars = int(usable_width / 4)

    for line in text:
        if y <= margin:
            c.showPage()
            y = height - margin

        # if line is too long, split it into chunks
        chunks = [line[i:i+max_chars] for i in range(0, len(line), max_chars)] or [""]

        for chunk in chunks:
            if y <= margin:
                c.showPage()
                y = height - margin
            c.drawString(x, y, chunk)
            y -= line_height

    c.save()
