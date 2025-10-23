#!/usr/bin/env python3
"""
Testar den flexibla Excel-läsaren på båda filerna
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from flexible_excel_reader import FlexibleLIAExcelReader

def test_flexible_reader():
    """Testar flexibla läsaren på båda Excel-filerna"""
    
    files_to_test = [
        "data/exempel_data.xlsx",
        "data/results_for_survey_586559445.xlsx"
    ]
    
    for file_path in files_to_test:
        if not os.path.exists(file_path):
            print(f"⚠️  Fil saknas: {file_path}")
            continue
            
        print(f"\n{'='*60}")
        print(f"🧪 TESTAR: {file_path}")
        print(f"{'='*60}")
        
        try:
            # Skapa läsare
            reader = FlexibleLIAExcelReader(file_path)
            
            # Ladda fil
            if not reader.load_excel():
                print("❌ Kunde inte ladda Excel-fil")
                continue
            
            # Analysera struktur
            if not reader.auto_detect_structure():
                print("❌ Kunde inte analysera struktur")
                continue
            
            # Extrahera data
            if not reader.extract_student_data():
                print("❌ Kunde inte extrahera studentdata")
                continue
            
            # Visa resultat
            summary = reader.get_structure_summary()
            print(f"\n📊 RESULTAT:")
            print(f"  Studenter: {summary['total_students']}")
            print(f"  Bedömningsområden: {summary['assessment_areas_count']}")
            
            print(f"\n🗂️  IDENTIFIERADE KOLUMNER:")
            for key, value in summary['basic_columns'].items():
                print(f"  {key}: {value}")
            
            print(f"\n📝 BEDÖMNINGSOMRÅDEN:")
            for i, area in enumerate(summary['assessment_areas'][:5], 1):  # Visa första 5
                desc = reader._extract_description_from_column(area['question_column'])
                print(f"  {i}. {desc[:60]}...")
            
            if summary['assessment_areas_count'] > 5:
                print(f"  ... och {summary['assessment_areas_count'] - 5} till")
            
            # Visa exempel på första studenten
            if reader.students_data:
                student = reader.students_data[0]
                print(f"\n👤 EXEMPEL STUDENT:")
                print(f"  Namn: {student.get('student_name', 'N/A')}")
                print(f"  Företag: {student.get('company', 'N/A')}")
                print(f"  Handledare: {student.get('supervisor', 'N/A')}")
                print(f"  Slutbetyg: {student.get('final_grade', 'N/A')}")
                print(f"  Antal bedömningar: {len(student.get('assessments', []))}")
            
            print("✅ Framgångsrikt testad!")
            
        except Exception as e:
            print(f"❌ Fel under test: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_flexible_reader()
    input("\nTryck Enter för att avsluta...")