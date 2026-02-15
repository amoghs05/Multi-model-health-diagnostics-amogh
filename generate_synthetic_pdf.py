from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_blood_report_pdf(filename="synthetic_blood_report.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 50

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "SYNTHETIC BLOOD TEST REPORT")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Patient Name: John Doe")
    y -= 20
    c.drawString(50, y, f"Age: 45")
    y -= 20
    c.drawString(50, y, f"Report Date: {datetime.now().strftime('%d-%m-%Y')}")
    y -= 30

    # Table Header
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Test")
    c.drawString(220, y, "Result")
    c.drawString(300, y, "Unit")
    c.drawString(380, y, "Reference Range")
    y -= 15

    c.line(50, y, 550, y)
    y -= 15

    c.setFont("Helvetica", 11)

    tests = [
        ("Hemoglobin", "12.2", "g/dL", "13.0 - 17.0"),
        ("WBC", "14500", "/µL", "4000 - 11000"),
        ("Platelet Count", "98000", "/µL", "150000 - 450000"),
        ("CRP", "38.5", "mg/L", "0 - 5"),
        ("RBC", "4.1", "million/µL", "4.5 - 5.9"),
    ]

    for test, value, unit, ref in tests:
        c.drawString(50, y, test)
        c.drawString(220, y, value)
        c.drawString(300, y, unit)
        c.drawString(380, y, ref)
        y -= 20

    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Remarks:")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, "• Elevated WBC and CRP suggest inflammation.")
    y -= 15
    c.drawString(50, y, "• Low platelet count observed.")

    c.showPage()
    c.save()

    print(f"Synthetic report created: {filename}")


if __name__ == "__main__":
    generate_blood_report_pdf()
