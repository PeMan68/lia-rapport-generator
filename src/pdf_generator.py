"""
PDF-generator för LIA-rapporter
Huvudmodul som genererar individuella PDF-rapporter från Excel-data
"""

import os
import logging
from typing import List, Dict
from datetime import datetime

# Importera våra moduler
from flexible_excel_reader import FlexibleLIAExcelReader
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'templates'))
from rapport_mall import LIAReportTemplate

# Konfigurera logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LIAPDFGenerator:
    """Huvudklass för att generera PDF-rapporter från Excel-data"""
    
    def __init__(self):
        self.excel_reader = None
        self.pdf_template = LIAReportTemplate()
        self.students_data = []
        
    def load_excel_file(self, file_path: str) -> bool:
        """
        Laddar Excel-fil och extraherar studentdata
        
        Args:
            file_path (str): Sökväg till Excel-fil
            
        Returns:
            bool: True om framgångsrik laddning
        """
        try:
            logger.info(f"Laddar Excel-fil: {file_path}")
            self.excel_reader = FlexibleLIAExcelReader(file_path)
            
            if not self.excel_reader.load_excel():
                logger.error("Kunde inte ladda Excel-fil")
                return False
            
            if not self.excel_reader.auto_detect_structure():
                logger.error("Kunde inte analysera Excel-struktur")
                return False
            
            if not self.excel_reader.extract_student_data():
                logger.error("Kunde inte extrahera studentdata")
                return False
            
            self.students_data = self.excel_reader.students_data
            
            if not self.students_data:
                logger.error("Ingen studentdata hittades i Excel-filen")
                return False
            
            logger.info(f"Framgångsrikt laddad data för {len(self.students_data)} studenter")
            return True
            
        except Exception as e:
            logger.error(f"Fel vid laddning av Excel-fil: {e}")
            return False
    
    def generate_all_reports(self, output_directory: str, practice_name: str = "", practice_period: str = "") -> Dict[str, str]:
        """
        Genererar PDF-rapporter för alla studenter
        
        Args:
            output_directory (str): Mapp där PDF-filer ska sparas
            practice_name (str): Namn på praktiken
            practice_period (str): Period för praktiken
            
        Returns:
            Dict[str, str]: Mapping av studentnamn till filsökvägar
        """
        if not self.students_data:
            logger.error("Ingen studentdata laddad")
            return {}
        
        # Skapa output-mapp om den inte finns
        os.makedirs(output_directory, exist_ok=True)
        logger.info(f"Sparar rapporter i: {output_directory}")
        
        generated_files = {}
        successful_count = 0
        
        for i, student in enumerate(self.students_data, 1):
            try:
                student_name = student.get('student_name', f'Student_{i}')
                logger.info(f"Genererar rapport {i}/{len(self.students_data)}: {student_name}")
                
                # Skapa säkert filnamn (ta bort specialtecken)
                safe_filename = self._create_safe_filename(student_name)
                output_path = os.path.join(output_directory, f"LIA_Rapport_{safe_filename}.pdf")
                
                # Generera PDF
                template = LIAReportTemplate()
                pdf_path = template.create_report(
                    student_data=student,
                    output_path=output_path,
                    practice_name=practice_name,
                    practice_period=practice_period
                )
                
                generated_files[student_name] = output_path
                successful_count += 1
                logger.info(f"✅ Rapport skapad: {output_path}")
                
            except Exception as e:
                logger.error(f"❌ Fel vid skapande av rapport för {student_name}: {e}")
                continue
        
        logger.info(f"🎉 Klart! {successful_count}/{len(self.students_data)} rapporter skapade")
        return generated_files
    
    def generate_single_report(self, student_name: str, output_path: str) -> bool:
        """
        Genererar PDF-rapport för en specifik student
        
        Args:
            student_name (str): Namn på student
            output_path (str): Sökväg där PDF ska sparas
            
        Returns:
            bool: True om framgångsrik generering
        """
        student_data = self.excel_reader.get_student_by_name(student_name)
        
        if not student_data:
            logger.error(f"Student '{student_name}' hittades inte")
            return False
        
        try:
            self.pdf_template.create_report(student_data, output_path)
            logger.info(f"✅ Rapport skapad för {student_name}: {output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Fel vid skapande av rapport för {student_name}: {e}")
            return False
    
    def get_students_list(self) -> List[str]:
        """
        Hämtar lista med studentnamn
        
        Returns:
            List[str]: Lista med studentnamn
        """
        return [student['student_name'] for student in self.students_data if student.get('student_name')]
    
    def get_students_summary(self) -> Dict:
        """
        Hämtar sammanfattning av studentdata
        
        Returns:
            Dict: Sammanfattning av data
        """
        if not self.students_data:
            return {}
        
        # Räkna betygsfördelning för helhetsintryck
        overall_grades = {}
        for student in self.students_data:
            grade = student.get('overall_impression', 'Okänt')
            overall_grades[grade] = overall_grades.get(grade, 0) + 1
        
        return {
            'total_students': len(self.students_data),
            'students': [student['student_name'] for student in self.students_data],
            'companies': list(set(student['company'] for student in self.students_data if student.get('company'))),
            'overall_grades_distribution': overall_grades
        }
    
    def _create_safe_filename(self, name: str) -> str:
        """
        Skapar säkert filnamn genom att ta bort specialtecken
        
        Args:
            name (str): Original namn
            
        Returns:
            str: Säkert filnamn
        """
        # Ersätt svenska tecken
        replacements = {
            'å': 'a', 'ä': 'a', 'ö': 'o',
            'Å': 'A', 'Ä': 'A', 'Ö': 'O'
        }
        
        safe_name = name
        for old, new in replacements.items():
            safe_name = safe_name.replace(old, new)
        
        # Ta bort eller ersätt andra specialtecken
        safe_chars = []
        for char in safe_name:
            if char.isalnum() or char in [' ', '-', '_']:
                safe_chars.append(char)
            else:
                safe_chars.append('_')
        
        # Ersätt mellanslag med understreck och begränsa längd
        safe_name = ''.join(safe_chars).replace(' ', '_')
        return safe_name[:50]  # Begränsa till 50 tecken
    
    def validate_excel_structure(self, file_path: str) -> Dict[str, any]:
        """
        Validerar Excel-filens struktur innan processing
        
        Args:
            file_path (str): Sökväg till Excel-fil
            
        Returns:
            Dict: Valideringsresultat
        """
        try:
            temp_reader = FlexibleLIAExcelReader(file_path)
            if not temp_reader.load_excel():
                return {'valid': False, 'error': 'Kunde inte läsa Excel-fil'}
            
            if not temp_reader.auto_detect_structure():
                return {'valid': False, 'error': 'Kunde inte analysera Excel-struktur'}
            
            if not temp_reader.extract_student_data():
                return {'valid': False, 'error': 'Kunde inte extrahera studentdata'}
            
            students = temp_reader.students_data
            if not students:
                return {'valid': False, 'error': 'Ingen studentdata hittades'}
            
            return {
                'valid': True,
                'student_count': len(students),
                'students': [s['student_name'] for s in students[:5]],  # Visa första 5
                'has_more': len(students) > 5
            }
            
        except Exception as e:
            return {'valid': False, 'error': f'Fel vid validering: {str(e)}'}


def main():
    """Testfunktion för PDF-generatorn"""
    generator = LIAPDFGenerator()
    
    # Testfil
    excel_file = "../data/exempel_data.xlsx"
    output_dir = "../output"
    
    print("🎯 TESTER PDF-GENERATOR")
    print("=" * 40)
    
    # Test 1: Validera Excel-struktur
    print("📋 Test 1: Validerar Excel-struktur...")
    validation = generator.validate_excel_structure(excel_file)
    if validation['valid']:
        print(f"✅ Excel-fil är giltig: {validation['student_count']} studenter")
        print(f"   Exempel studenter: {', '.join(validation['students'])}")
    else:
        print(f"❌ Excel-fil ogiltig: {validation['error']}")
        return
    
    # Test 2: Ladda data
    print("\n📂 Test 2: Laddar Excel-data...")
    if generator.load_excel_file(excel_file):
        summary = generator.get_students_summary()
        print(f"✅ Data laddad: {summary['total_students']} studenter")
        print(f"   Företag: {len(summary['companies'])} olika")
    else:
        print("❌ Kunde inte ladda Excel-data")
        return
    
    # Test 3: Generera en rapport
    print("\n📄 Test 3: Genererar en test-rapport...")
    students = generator.get_students_list()
    if students:
        test_output = os.path.join(output_dir, "test_rapport_en_student.pdf")
        if generator.generate_single_report(students[0], test_output):
            print(f"✅ Test-rapport skapad: {test_output}")
        else:
            print("❌ Kunde inte skapa test-rapport")
    
    # Test 4: Generera alla rapporter
    print("\n📊 Test 4: Genererar alla rapporter...")
    generated_files = generator.generate_all_reports(output_dir)
    
    if generated_files:
        print(f"✅ {len(generated_files)} rapporter skapade:")
        for student, filepath in generated_files.items():
            print(f"   📄 {student}: {os.path.basename(filepath)}")
    else:
        print("❌ Inga rapporter skapades")
    
    print(f"\n🎉 Test slutfört! Kontrollera mappen: {output_dir}")


if __name__ == "__main__":
    main()