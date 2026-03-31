from io import BytesIO
from decimal import Decimal

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def fmt_money(value):
    if value is None:
        return "0.00"
    return f"{Decimal(value):,.2f} EUR"


def build_early_repayment_pdf(results, cleaned_data):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    story = []

    title = "Early Repayment Report"
    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Input data", styles["Heading2"]))
    story.append(Paragraph(
        f"Current principal: {fmt_money(cleaned_data['current_principal'])}", styles["Normal"]
    ))
    story.append(Paragraph(
        f"Yearly interest rate: {cleaned_data['yearly_interest_rate']}%", styles["Normal"]
    ))
    story.append(Paragraph(
        f"Years left: {cleaned_data['years_left']}", styles["Normal"]
    ))
    story.append(Paragraph(
        f"Current monthly payment: {fmt_money(cleaned_data['monthly_payment'])}", styles["Normal"]
    ))
    story.append(Paragraph(
        f"New monthly payment: {fmt_money(cleaned_data['early_monthly_payment'])}", styles["Normal"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Key results", styles["Heading2"]))
    story.append(Paragraph(
        f"Total money saved: {fmt_money(results['savings']['total_paid_saved'])}", styles["Normal"]
    ))
    story.append(Paragraph(
        f"Interest saved: {fmt_money(results['savings']['interest_saved'])}", styles["Normal"]
    ))
    story.append(Paragraph(
        f"New repayment time: {results['early']['years']} years and "
        f"{results['early']['remaining_months']} months",
        styles["Normal"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Original plan", styles["Heading2"]))
    story.append(Paragraph(
        f"Total paid: {fmt_money(results['original']['total_paid'])}", styles["Normal"]
    ))
    story.append(Paragraph(
        f"Interest + insurance + fees: {fmt_money(results['original']['extra_costs_total'])}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Early repayment plan", styles["Heading2"]))
    story.append(Paragraph(
        f"Total paid: {fmt_money(results['early']['total_paid'])}", styles["Normal"]
    ))
    story.append(Paragraph(
        f"Interest + insurance + fees: {fmt_money(results['early']['extra_costs_total'])}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Savings breakdown", styles["Heading2"]))
    story.append(Paragraph(
        f"Life insurance saved: {fmt_money(results['savings']['life_insurance_saved'])}",
        styles["Normal"]
    ))
    story.append(Paragraph(
        f"Property insurance saved: {fmt_money(results['savings']['property_insurance_saved'])}",
        styles["Normal"]
    ))
    story.append(Paragraph(
        f"Bank fees saved: {fmt_money(results['savings']['bank_fees_saved'])}",
        styles["Normal"]
    ))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes