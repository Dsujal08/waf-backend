import pandas as pd
import io
from reportlab.pdfgen import canvas
from flask import send_file
from datetime import datetime

def export_csv_from_rows(rows):
    df = pd.DataFrame(rows)
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return send_file(io.BytesIO(buf.getvalue().encode()), mimetype="text/csv",
                     download_name=f"export_{int(datetime.utcnow().timestamp())}.csv")

def export_json_from_rows(rows):
    import json, io
    buf = io.StringIO()
    json.dump(rows, buf, indent=2, default=str)
    buf.seek(0)
    return send_file(io.BytesIO(buf.getvalue().encode()), mimetype="application/json",
                     download_name=f"export_{int(datetime.utcnow().timestamp())}.json")

def export_pdf_from_rows(rows):
    import io
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    y=800
    for i, r in enumerate(rows[:200]):
        c.drawString(30,y, f"{i+1}. {r}")
        y -= 12
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf",
                     download_name=f"export_{int(datetime.utcnow().timestamp())}.pdf")
