#!/usr/bin/env python3
"""
Testar LIA-borttagning från praktiknamn i filnamn
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from flexible_excel_reader import FlexibleLIAExcelReader
from pdf_generator import LIAPDFGenerator

def test_lia_removal_in_filenames():
    """Testar att LIA tas bort från praktiknamn i filnamn"""
    print("🧪 Testar LIA-borttagning från filnamn...")
    
    # Testa olika praktiknamn med LIA
    test_cases = [
        {
            "practice_name": "LIA Webbutveckling",
            "expected_contains": "Webbutveckling",
            "expected_not_contains": "LIA_LIA"
        },
        {
            "practice_name": "LIA-Processteknik HT2024",
            "expected_contains": "Processteknik_HT2024",
            "expected_not_contains": "LIA_LIA"
        },
        {
            "practice_name": "Webbutveckling LIA vårterminen",
            "expected_contains": "Webbutveckling",
            "expected_not_contains": "LIA_LIA"
        },
        {
            "practice_name": "LIA",  # Endast LIA
            "expected_contains": "LIA_",
            "expected_not_contains": "LIA_LIA"
        },
        {
            "practice_name": "Automation utan LIA",
            "expected_contains": "Automation_utan",
            "expected_not_contains": "LIA_LIA"
        }
    ]
    
    excel_path = "data/exempel_data.xlsx"
    if not os.path.exists(excel_path):
        print("❌ Ingen testdata hittades")
        return False
    
    try:
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: '{test_case['practice_name']}'")
            
            # Skapa generator och ladda data
            generator = LIAPDFGenerator()
            if not generator.load_excel_file(excel_path):
                print("❌ Kunde inte ladda Excel-data")
                continue
            
            # Skapa output-mapp för test
            output_dir = f"output/test_lia_removal_{i}"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generera bara en rapport för att testa filnamnet
            if generator.students_data:
                # Testa direkt på första studenten
                student = generator.students_data[0]
                student_name = student.get('student_name', 'Test_Student')
                
                # Simulera filnamnsskapande
                safe_student_name = generator._create_safe_filename(student_name)
                
                # Skapa säkert praktiknamn (samma logik som i generate_all_reports)
                safe_practice_name = ""
                if test_case['practice_name']:
                    import re
                    cleaned_practice_name = test_case['practice_name']
                    cleaned_practice_name = re.sub(r'\bLIA\b[-\s]*', '', cleaned_practice_name, flags=re.IGNORECASE)
                    cleaned_practice_name = cleaned_practice_name.strip()
                    
                    if cleaned_practice_name:
                        safe_practice_name = generator._create_safe_filename(cleaned_practice_name)
                        safe_practice_name = safe_practice_name[:20]
                        safe_practice_name = f"{safe_practice_name}_"
                
                # Skapa filnamn
                filename = f"LIA_{safe_practice_name}{safe_student_name}.pdf"
                
                print(f"   Original: '{test_case['practice_name']}'")
                print(f"   Filnamn: '{filename}'")
                
                # Kontrollera förväntningar
                if test_case['expected_contains'] in filename:
                    print(f"   ✅ Innehåller '{test_case['expected_contains']}'")
                else:
                    print(f"   ❌ Saknar '{test_case['expected_contains']}'")
                
                if test_case['expected_not_contains'] not in filename:
                    print(f"   ✅ Innehåller INTE '{test_case['expected_not_contains']}'")
                else:
                    print(f"   ❌ Innehåller felaktigt '{test_case['expected_not_contains']}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Fel under test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_lia_removal_in_filenames()
    if success:
        print("\n🎉 LIA-borttagningstest genomfört!")
    else:
        print("\n💥 Test misslyckades")
    
    input("\nTryck Enter för att avsluta...")