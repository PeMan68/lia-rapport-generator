"""
Excel Reader för LIA-rapporter
Läser och parsar Excel-fil med studentomdömen från LIA-praktik
"""

import pandas as pd
from typing import Dict, List, Optional
import logging

# Konfigurera logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LIAExcelReader:
    """Klass för att läsa och bearbeta LIA-rapporter från Excel"""
    
    def __init__(self, file_path: str):
        """
        Initialiserar Excel-läsaren
        
        Args:
            file_path (str): Sökväg till Excel-filen
        """
        self.file_path = file_path
        self.df = None
        self.students_data = []
        
    def load_excel(self) -> bool:
        """
        Laddar Excel-filen
        
        Returns:
            bool: True om fil laddades framgångsrikt, False annars
        """
        try:
            logger.info(f"Laddar Excel-fil: {self.file_path}")
            self.df = pd.read_excel(self.file_path)
            logger.info(f"Fil laddad framgångsrikt. Antal rader: {len(self.df)}")
            return True
        except Exception as e:
            logger.error(f"Fel vid laddning av Excel-fil: {e}")
            return False
    
    def validate_structure(self) -> bool:
        """
        Validerar att Excel-filen har rätt struktur
        
        Returns:
            bool: True om strukturen är korrekt
        """
        if self.df is None:
            logger.error("Excel-fil inte laddad")
            return False
            
        required_columns = [
            'Q1: Namn Yh-studerande',
            'Q2: Namn företag',
            'Q3: Namn handledare',
            'Q33: Helhetsintryck'
        ]
        
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        
        if missing_columns:
            logger.error(f"Saknade kolumner: {missing_columns}")
            return False
            
        logger.info("Excel-struktur validerad framgångsrikt")
        return True
    
    def extract_student_data(self) -> List[Dict]:
        """
        Extraherar studentdata från Excel-filen
        
        Returns:
            List[Dict]: Lista med studentdata
        """
        if not self.validate_structure():
            return []
        
        students = []
        
        for index, row in self.df.iterrows():
            student_data = {
                'index': index,
                'student_name': self._clean_text(row.get('Q1: Namn Yh-studerande', '')),
                'company': self._clean_text(row.get('Q2: Namn företag', '')),
                'supervisor': self._clean_text(row.get('Q3: Namn handledare', '')),
                'attendance': self._clean_text(row.get('Q4: Närvarotimmar vid företaget', '')),
                'overall_impression': self._clean_text(row.get('Q33: Helhetsintryck', '')),
                'final_comments': self._clean_text(row.get('Q34: Kommentarer', '')),
                'assessments': self._extract_assessments(row)
            }
            
            # Skippa rader utan studentnamn
            if student_data['student_name']:
                students.append(student_data)
                logger.info(f"Student extraherad: {student_data['student_name']}")
        
        self.students_data = students
        logger.info(f"Totalt {len(students)} studenter extraherade")
        return students
    
    def _extract_assessments(self, row: pd.Series) -> List[Dict]:
        """
        Extraherar bedömningsdata för en student
        
        Args:
            row (pd.Series): Rad från DataFrame
            
        Returns:
            List[Dict]: Lista med bedömningar
        """
        assessments = []
        
        # Definiera bedömningsområden med kolumnnamn
        assessment_areas = [
            {
                'name': 'Arbetets kvalitet',
                'description': 'Noggrannhet, omsorg i arbetet',
                'grade_col': 'Q5: Arbetets kvalitet. \nNoggrannhet, omsorg i arbetet.',
                'comment_col': 'Q6: Kommentar'
            },
            {
                'name': 'Arbetstider',
                'description': '',
                'grade_col': 'Q7: Arbetstider',
                'comment_col': 'Q8: Kommentar'
            },
            {
                'name': 'Kreativitet',
                'description': 'Förmåga att sätta sig in i nya arbetsuppgifter',
                'grade_col': 'Q9: Kreativitet \nFörmåga att sätta sig in i nya arbetsuppgifter',
                'comment_col': 'Q10: Kommentar'
            },
            {
                'name': 'Intresse för arbetet',
                'description': '',
                'grade_col': 'Q11: Intresse för arbetet',
                'comment_col': 'Q12: Kommentar'
            },
            {
                'name': 'Initiativförmåga',
                'description': 'Företagsamhet, självständighet',
                'grade_col': 'Q13: Initiativförmåga \nFöretagsamhet, självständighet',
                'comment_col': 'Q14: Kommentar'
            },
            {
                'name': 'Samarbetsförmåga',
                'description': '',
                'grade_col': 'Q15: Samarbetsförmåga',
                'comment_col': 'Q16: Kommentar'
            },
            {
                'name': 'Kunskap om risker',
                'description': 'Kunskap om de risker som finns med elarbete',
                'grade_col': 'Q17: Kunskap om de risker som finns med elarbete',
                'comment_col': 'Q18: Kommentar'
            },
            {
                'name': 'Eldistribution',
                'description': 'Kunskap om hur elen distribueras och transformeras',
                'grade_col': 'Q19: Kunskap om hur elen distribueras och transformeras i en industrianläggning',
                'comment_col': 'Q20: Kommentar'
            },
            {
                'name': 'Dokumentation',
                'description': 'Kunskap om el-konstruktörsdokumentation',
                'grade_col': 'Q21: Kunskap om hur dokumentationen som produceras av en el-konstruktör används',
                'comment_col': 'Q22: Kommentar'
            },
            {
                'name': 'Problemredogörelse',
                'description': 'Färdighet att redogöra för vanligaste problemen',
                'grade_col': 'Q23: Färdighet i att redogöra för de vanligaste problemen inom el-området',
                'comment_col': 'Q24: Kommentar'
            },
            {
                'name': 'Felsökning',
                'description': 'Färdighet i att felsöka på el-utrustning',
                'grade_col': 'Q25: Färdighet i att felsöka på el-utrustning',
                'comment_col': 'Q26: Kommentar'
            },
            {
                'name': 'Säkerhetskunskap',
                'description': 'Färdighet att skydda sig mot risker',
                'grade_col': 'Q27: Färdighet i att skydda sig mot de risker som är förknippade med el-underhåll',
                'comment_col': 'Q28: Kommentar'
            },
            {
                'name': 'Installation och drift',
                'description': 'Färdighet att installera automationsutrustning',
                'grade_col': 'Q29: Färdighet i att installera och ta i drift automationsutrustning',
                'comment_col': 'Q30: Kommentar'
            },
            {
                'name': 'Förebyggande underhåll',
                'description': 'Kompetens att utföra underhåll',
                'grade_col': 'Q31: Kompetens att utföra förebyggande och avhjälpande underhåll',
                'comment_col': 'Q32: Kommentar'
            }
        ]
        
        for area in assessment_areas:
            grade = self._clean_text(row.get(area['grade_col'], ''))
            comment = self._clean_text(row.get(area['comment_col'], ''))
            
            assessments.append({
                'name': area['name'],
                'description': area['description'],
                'grade': grade,
                'comment': comment,
                'grade_numeric': self._grade_to_numeric(grade)
            })
        
        return assessments
    
    def _clean_text(self, text) -> str:
        """
        Rengör text från NaN och whitespace
        
        Args:
            text: Text att rengöra
            
        Returns:
            str: Rengjord text
        """
        if pd.isna(text):
            return ''
        return str(text).strip()
    
    def _grade_to_numeric(self, grade: str) -> int:
        """
        Konverterar textbetyg till numeriskt värde
        
        Args:
            grade (str): Textbetyg
            
        Returns:
            int: Numeriskt betyg (1-3) eller 0 för okänt
        """
        grade_lower = grade.lower()
        if '3' in grade_lower or 'mycket bra' in grade_lower:
            return 3
        elif '2' in grade_lower or 'bra' in grade_lower:
            return 2
        elif '1' in grade_lower or 'förbättras' in grade_lower:
            return 1
        else:
            return 0
    
    def get_student_by_name(self, name: str) -> Optional[Dict]:
        """
        Hämtar studentdata baserat på namn
        
        Args:
            name (str): Studentens namn
            
        Returns:
            Optional[Dict]: Studentdata eller None
        """
        for student in self.students_data:
            if student['student_name'].lower() == name.lower():
                return student
        return None
    
    def get_all_students(self) -> List[Dict]:
        """
        Hämtar alla studenters data
        
        Returns:
            List[Dict]: Lista med all studentdata
        """
        return self.students_data
    
    def print_summary(self):
        """Skriver ut en sammanfattning av inläst data"""
        if not self.students_data:
            print("Ingen studentdata hittad")
            return
        
        print(f"\n📊 SAMMANFATTNING AV INLÄST DATA")
        print("=" * 50)
        print(f"Antal studenter: {len(self.students_data)}")
        print(f"Antal bedömningsområden: {len(self.students_data[0]['assessments']) if self.students_data else 0}")
        
        print(f"\n👥 STUDENTER:")
        for i, student in enumerate(self.students_data, 1):
            print(f"{i:2d}. {student['student_name']} - {student['company']}")
        
        print(f"\n🎯 HELHETSINTRYCK FÖRDELNING:")
        impression_counts = {}
        for student in self.students_data:
            impression = student['overall_impression']
            impression_counts[impression] = impression_counts.get(impression, 0) + 1
        
        for impression, count in impression_counts.items():
            if impression:
                print(f"   {impression}: {count} studenter")


def main():
    """Testfunktion för Excel-läsaren"""
    # Testa med anonymiserad Excel-fil
    reader = LIAExcelReader("../data/exempel_data.xlsx")
    
    if reader.load_excel():
        students = reader.extract_student_data()
        reader.print_summary()
        
        # Visa detaljerad info för första studenten
        if students:
            print(f"\n📋 DETALJERAD INFO - {students[0]['student_name']}")
            print("=" * 50)
            student = students[0]
            print(f"Företag: {student['company']}")
            print(f"Handledare: {student['supervisor']}")
            print(f"Närvarotid: {student['attendance']}")
            print(f"Helhetsintryck: {student['overall_impression']}")
            
            print(f"\nBedömningar:")
            for assessment in student['assessments'][:3]:  # Visa bara första 3
                print(f"  {assessment['name']}: {assessment['grade']}")
                if assessment['comment']:
                    print(f"    Kommentar: {assessment['comment']}")


if __name__ == "__main__":
    main()