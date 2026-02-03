"""
PDF Generator Utility
Generates professional claim letters using ReportLab
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

class PDFGenerator:
    """
    Generates PDF claim documents
    """

    def __init__(self, output_dir='generated_claims'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_claim_letter(self, data: dict, filename: str = None) -> str:
        """
        Generate a PDF claim letter

        Args:
            data: Dictionary containing claim details
            filename: Optional filename (default: claim_{ref}.pdf)

        Returns:
            Path to the generated PDF file
        """
        if not filename:
            ref = data.get('claim_reference', 'draft')
            filename = f"claim_{ref}.pdf"

        filepath = os.path.join(self.output_dir, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=4, spaceAfter=12))

        # Content
        story = []

        # Title
        title = Paragraph("<b>FLIGHT COMPENSATION CLAIM</b><br/>UNDER DGCA CAR SECTION 3", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.5*inch))

        # Header Info
        date_str = datetime.now().strftime("%d %B %Y")
        header_text = f"""
        <b>Date:</b> {date_str}<br/>
        <b>Claim Reference:</b> {data.get('claim_reference', 'PENDING')}<br/>
        <br/>
        <b>TO:</b> Customer Relations Department<br/>
        <b>Airline:</b> {data.get('airline_name', 'The Airline')}
        """
        story.append(Paragraph(header_text, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))

        # Subject
        subject = Paragraph(
            "<b>SUBJECT: Claim for Compensation under DGCA CAR Section 3, Series M, Part IV</b>",
            styles['Normal']
        )
        story.append(subject)
        story.append(Spacer(1, 0.2*inch))

        # Body
        body_intro = """
        Dear Sir/Madam,
        <br/><br/>
        I am writing to file a formal claim for compensation for the disruption to my flight as detailed below.
        According to the Directorate General of Civil Aviation (DGCA) Civil Aviation Requirements (CAR)
        Section 3, Series M, Part IV, I am entitled to compensation.
        """
        story.append(Paragraph(body_intro, styles['Justify']))
        story.append(Spacer(1, 0.2*inch))

        # Flight Details Table
        flight_data = [
            ['Passenger Name', data.get('passenger_name', 'N/A')],
            ['Flight Number', data.get('flight_number', 'N/A')],
            ['Date of Travel', data.get('flight_date', 'N/A')],
            ['Route', f"{data.get('route_from', 'N/A')} to {data.get('route_to', 'N/A')}"],
            ['Disruption Type', str(data.get('disruption_type', 'Delay')).upper()],
            ['Duration', f"{data.get('delay_hours', 'N/A')} hours"]
        ]

        t = Table(flight_data, colWidths=[2*inch, 3*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey)
        ]))
        story.append(t)
        story.append(Spacer(1, 0.3*inch))

        # Legal Argument
        amount = f"{data.get('compensation_amount', 0):,}"
        legal_text = f"""
        My flight was delayed/cancelled for reasons within the airline's control.
        As per DGCA regulations, for a flight of this duration and delay magnitude,
        passengers are entitled to a compensation of <b>INR {amount}</b>.
        <br/><br/>
        I request you to process this compensation and credit the amount to my bank account
        within 30 days of receipt of this letter.
        """
        story.append(Paragraph(legal_text, styles['Justify']))
        story.append(Spacer(1, 0.2*inch))

        # Closing
        closing = f"""
        Sincerely,
        <br/><br/>
        <b>{data.get('passenger_name', 'Passenger')}</b><br/>
        Email: {data.get('passenger_email', 'N/A')}<br/>
        Phone: {data.get('passenger_phone', 'N/A')}
        """
        story.append(Paragraph(closing, styles['Normal']))

        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(
            "<font size=8 color=grey>Generated by FlyClaim AI - Automated Flight Compensation System</font>",
            styles['Normal']
        )
        story.append(footer)

        # Build
        doc.build(story)
        return filepath

# Test
if __name__ == "__main__":
    generator = PDFGenerator()
    test_data = {
        'claim_reference': 'TEST-001',
        'airline_name': 'IndiGo',
        'passenger_name': 'Rahul Kumar',
        'flight_number': '6E-234',
        'flight_date': '2025-10-28',
        'route_from': 'Delhi',
        'route_to': 'Mumbai',
        'disruption_type': 'Delay',
        'delay_hours': 5,
        'compensation_amount': 10000,
        'passenger_email': 'rahul@example.com',
        'passenger_phone': '+91 98765 43210'
    }
    path = generator.generate_claim_letter(test_data)
    print(f"Generated PDF at: {path}")
