import pandas as pd
from reportlab.pdfgen import canvas

def export_csv(data, path):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)

def export_json(data, path):
    df = pd.DataFrame(data)
    df.to_json(path, orient="records")

def export_pdf(data, path):
    c = canvas.Canvas(path)
    c.drawString(50, 800, "Exported Data PDF")
    y = 780
    for row in data:
        c.drawString(50, y, str(row))
        y -= 20
    c.save()
