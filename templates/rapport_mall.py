"""
PDF-rapportmall för LIA-rapporter
Skapar professionella PDF-rapporter från studentdata
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os

class LIAReportTemplate:
    """Klass för att skapa PDF-rapporter från LIA-data"""
    
    def __init__(self):
        self.setup_styles()
        
    def setup_styles(self):
        """Konfigurerar stilar för PDF-rapporten"""
        self.styles = getSampleStyleSheet()
        
        # Anpassade stilar
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            textColor=colors.HexColor('#2C3E50'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#34495E'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Helvetica'
        ))
        
        self.styles.add(ParagraphStyle(
            name='Comment',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=4,
            leftIndent=20,
            fontName='Helvetica',
            textColor=colors.black
        ))
    
    def create_report(self, student_data, output_path, practice_name="", practice_period=""):
        """
        Skapar en PDF-rapport för en student
        
        Args:
            student_data (dict): Studentdata från Excel-läsaren
            output_path (str): Sökväg där PDF ska sparas
            practice_name (str): Namn på praktiken
            practice_period (str): Period för praktiken
        """
        # Skapa output-mapp om den inte finns
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Skapa PDF-dokument
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Bygg innehåll
        story = []
        
        # Rubrik med praktikinfo
        title_parts = ["PRAKTIKRAPPORT - LIA"]
        if practice_name:
            title_parts.append(f"<br/>{practice_name}")
        if practice_period:
            title_parts.append(f"<br/>Period: {practice_period}")
        
        title_text = "".join(title_parts)
        story.append(Paragraph(title_text, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Grundinfo
        story.extend(self._create_basic_info_section(student_data, practice_name, practice_period))
        
        # Bedömningar
        story.extend(self._create_assessments_section(student_data))
        
        # Sammanfattning
        story.extend(self._create_summary_section(student_data))
        
        # Generera PDF
        doc.build(story)
        
    def _create_basic_info_section(self, student_data, practice_name="", practice_period=""):
        """Skapar grundinformation-sektionen"""
        content = []
        
        content.append(Paragraph("► PRAKTIKPLATS", self.styles['SectionHeader']))
        
        # Grunddata tabell med praktikinfo
        basic_data = [
            ['Student:', student_data.get('student_name', '')],
            ['Företag:', student_data.get('company', '')],
            ['Handledare:', student_data.get('supervisor', '')],
            ['Närvarotid:', student_data.get('attendance', '')]
        ]
        
        # Lägg till praktikinfo om det finns
        if practice_name:
            basic_data.append(['Praktiknamn:', practice_name])
        if practice_period:
            basic_data.append(['Period:', practice_period])
        
        basic_table = Table(basic_data, colWidths=[4*cm, 12*cm])
        basic_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        content.append(basic_table)
        content.append(Spacer(1, 20))
        
        return content
    
    def _create_assessments_section(self, student_data):
        """Skapar bedömnings-sektionen"""
        content = []
        
        content.append(Paragraph("► BEDÖMNING", self.styles['SectionHeader']))
        
        assessments = student_data.get('assessments', [])
        
        for assessment in assessments:
            # Område namn och betyg
            grade_text = self._format_grade(assessment.get('grade', ''))
            area_text = f"<b>{assessment.get('name', '')}</b>"
            if assessment.get('description'):
                area_text += f" - {assessment.get('description', '')}"
            
            content.append(Paragraph(area_text, self.styles['SubHeader']))
            content.append(Paragraph(f"<b>Betyg:</b> {grade_text}", self.styles['CustomBodyText']))
            
            # Kommentar om den finns
            comment = assessment.get('comment', '').strip()
            if comment:
                content.append(Paragraph(f"<b>Kommentar:</b> {comment}", self.styles['Comment']))
            
            content.append(Spacer(1, 8))
        
        return content
    
    def _create_summary_section(self, student_data):
        """Skapar sammanfattnings-sektionen"""
        content = []
        
        content.append(Paragraph("► SAMMANFATTNING", self.styles['SectionHeader']))
        
        # Helhetsintryck
        overall = student_data.get('overall_impression', '')
        overall_formatted = self._format_grade(overall)
        content.append(Paragraph(f"<b>Helhetsintryck:</b> {overall_formatted}", self.styles['CustomBodyText']))
        
        # Avslutande kommentarer
        final_comments = student_data.get('final_comments', '').strip()
        if final_comments:
            content.append(Spacer(1, 12))
            content.append(Paragraph("<b>Avslutande kommentarer:</b>", self.styles['SubHeader']))
            content.append(Paragraph(final_comments, self.styles['CustomBodyText']))
        
        # Betygsstatistik
        content.append(Spacer(1, 20))
        content.extend(self._create_grade_statistics(student_data))
        
        # Datum
        content.append(Spacer(1, 30))
        today = datetime.now().strftime("%d %B %Y")
        content.append(Paragraph(f"<i>Rapport genererad: {today}</i>", self.styles['Comment']))
        
        return content
    
    def _create_grade_statistics(self, student_data):
        """Skapar betygsstatistik"""
        content = []
        
        assessments = student_data.get('assessments', [])
        if not assessments:
            return content
        
        # Räkna betyg
        grade_counts = {'3 Mycket bra': 0, '2 Bra': 0, '1 Bör förbättras': 0, 'Ej bedömt': 0}
        
        for assessment in assessments:
            grade = assessment.get('grade', '').strip()
            if not grade:
                grade_counts['Ej bedömt'] += 1
            elif '3' in grade.lower() or 'mycket bra' in grade.lower():
                grade_counts['3 Mycket bra'] += 1
            elif '2' in grade.lower() or 'bra' in grade.lower():
                grade_counts['2 Bra'] += 1
            elif '1' in grade.lower() or 'förbättras' in grade.lower():
                grade_counts['1 Bör förbättras'] += 1
            else:
                grade_counts['Ej bedömt'] += 1
        
        content.append(Paragraph("▪ BETYGSFÖRDELNING", self.styles['SubHeader']))
        
        # Skapa statistik-tabell
        stats_data = []
        for grade, count in grade_counts.items():
            if count > 0:
                percentage = (count / len(assessments)) * 100
                stats_data.append([grade, str(count), f"{percentage:.0f}%"])
        
        if stats_data:
            # Lägg till headers
            stats_data.insert(0, ['Betyg', 'Antal', 'Andel'])
            
            stats_table = Table(stats_data, colWidths=[6*cm, 2*cm, 2*cm])
            stats_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ECF0F1')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            content.append(stats_table)
        
        return content
    
    def _format_grade(self, grade):
        """Formaterar betyg enkelt utan extra symboler"""
        if not grade:
            return "Ej bedömt"
        
        # Returnera betyget som det är - det innehåller redan all nödvändig info
        return grade.strip()


def main():
    """Testfunktion för PDF-mall"""
    # Importera Excel-läsaren för testdata
    import sys
    sys.path.append('.')
    from src.excel_reader import LIAExcelReader
    
    # Läs testdata
    reader = LIAExcelReader("data/exempel_data.xlsx")
    if reader.load_excel():
        students = reader.extract_student_data()
        
        if students:
            # Skapa PDF för första studenten
            template = LIAReportTemplate()
            output_path = "output/test_rapport.pdf"
            
            print(f"🎨 Skapar PDF-rapport för: {students[0]['student_name']}")
            template.create_report(students[0], output_path)
            print(f"✅ PDF skapad: {output_path}")
        else:
            print("❌ Ingen studentdata hittad")
    else:
        print("❌ Kunde inte läsa Excel-fil")


if __name__ == "__main__":
    main()