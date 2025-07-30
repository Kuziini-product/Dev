import pandas as pd
from fpdf import FPDF
from pathlib import Path

def export_excel(deviz_data, nume_fisier):
    df = pd.DataFrame(deviz_data)
    df.to_excel(nume_fisier + ".xlsx", index=False)

def export_pdf(deviz_data, nume_fisier, logo_path="Kuziini_logo_negru.png"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if Path(logo_path).exists():
        pdf.image(logo_path, x=10, y=8, w=40)
        pdf.ln(30)
    else:
        pdf.ln(15)

    pdf.cell(200, 10, txt="Deviz ofertă Kuziini", ln=True, align="C")
    pdf.ln(10)

    col_widths = [60, 30, 25, 25, 25]
    headers = ["Produs", "Cod", "UM", "Cantitate", "Preț (lei)"]

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1)
    pdf.ln()

    total = 0
    for row in deviz_data:
        pdf.cell(col_widths[0], 10, row["Produs"], border=1)
        pdf.cell(col_widths[1], 10, row["Cod"], border=1)
        pdf.cell(col_widths[2], 10, row["UM"], border=1)
        pdf.cell(col_widths[3], 10, str(row["Cantitate"]), border=1)
        pdf.cell(col_widths[4], 10, f"{row['Pret']:.2f}", border=1)
        pdf.ln()
        total += row["Cantitate"] * row["Pret"]

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total general: {total:.2f} lei", ln=True, align="R")

    pdf.output(nume_fisier + ".pdf")