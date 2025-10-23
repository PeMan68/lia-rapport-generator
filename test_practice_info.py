#!/usr/bin/env python3
"""
Test script för att verifiera praktikinfo-funktionen
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from excel_reader import LIAExcelReader
from pdf_generator import LIAPDFGenerator

def test_practice_info():
    """Testar praktikinfo i PDF-generering"""
    print("🧪 Testar praktikinfo-funktionen...")
    
    # Ladda testdata
    excel_path = "data/exempel_data.xlsx"
    if not os.path.exists(excel_path):
        print("❌ Ingen testdata hittades")
        return False
    
    try:
        # Läs Excel-data
        reader = LIAExcelReader(excel_path)
        if not reader.load_excel():
            print("❌ Kunde inte ladda Excel-data")
            return False
        
        # Skapa generator och ladda data
        generator = LIAPDFGenerator()
        if not generator.load_excel_file(excel_path):
            print("❌ Kunde inte ladda Excel-data till generator")
            return False
        
        # Testa med praktikinfo
        test_practice_name = "Webbutveckling vårterminen"
        test_practice_period = "2024-03-01 till 2024-05-31"
        
        print(f"📝 Testar med praktiknamn: {test_practice_name}")
        print(f"📅 Testar med period: {test_practice_period}")
        
        # Skapa output-mapp för test
        output_dir = "output/test_practice_info"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generera rapporter med praktikinfo
        generated_files = generator.generate_all_reports(
            output_directory=output_dir,
            practice_name=test_practice_name,
            practice_period=test_practice_period
        )
        
        print(f"✅ Genererade {len(generated_files)} rapporter med praktikinfo")
        print("📁 Rapporter skapade i: output/test_practice_info/")
        
        # Lista skapade filer
        for student_name, file_path in generated_files.items():
            if os.path.exists(file_path):
                print(f"  ✓ {student_name}: {os.path.basename(file_path)}")
            else:
                print(f"  ❌ {student_name}: Fil kunde inte skapas")
        
        return True
        
    except Exception as e:
        print(f"❌ Fel under test: {e}")
        return False

if __name__ == "__main__":
    success = test_practice_info()
    if success:
        print("\n🎉 Test genomfört framgångsrikt!")
        print("🔍 Kontrollera PDF-filerna för att se om praktikinfo visas korrekt")
    else:
        print("\n💥 Test misslyckades")
    
    input("\nTryck Enter för att avsluta...")