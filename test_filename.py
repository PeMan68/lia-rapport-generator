#!/usr/bin/env python3
"""
Testar ny filnamngivning med praktiknamn
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from flexible_excel_reader import FlexibleLIAExcelReader
from pdf_generator import LIAPDFGenerator

def test_filename_with_practice_name():
    """Testar filnamngivning med praktiknamn"""
    print("🧪 Testar ny filnamngivning med praktiknamn...")
    
    # Testa olika praktiknamn
    test_cases = [
        {
            "practice_name": "Webbutveckling vårterminen",
            "practice_period": "VT 2024",
            "expected_prefix": "LIA_Webbutveckling_varte_"
        },
        {
            "practice_name": "Processteknik HT2024",
            "practice_period": "Hösttermin 2024",
            "expected_prefix": "LIA_Processteknik_HT2024_"
        },
        {
            "practice_name": "",
            "practice_period": "VT 2024",
            "expected_prefix": "LIA_"
        }
    ]
    
    excel_path = "data/exempel_data.xlsx"
    if not os.path.exists(excel_path):
        print("❌ Ingen testdata hittades")
        return False
    
    try:
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: {test_case['practice_name'] or 'Inget praktiknamn'}")
            
            # Skapa generator och ladda data
            generator = LIAPDFGenerator()
            if not generator.load_excel_file(excel_path):
                print("❌ Kunde inte ladda Excel-data")
                continue
            
            # Skapa output-mapp för test
            output_dir = f"output/test_filenames_{i}"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generera rapporter med praktikinfo
            generated_files = generator.generate_all_reports(
                output_directory=output_dir,
                practice_name=test_case['practice_name'],
                practice_period=test_case['practice_period']
            )
            
            print(f"✅ Genererade {len(generated_files)} rapporter")
            
            # Kontrollera filnamn
            sample_file = list(generated_files.values())[0] if generated_files else None
            if sample_file:
                filename = os.path.basename(sample_file)
                print(f"📁 Exempel filnamn: {filename}")
                
                # Kontrollera att filnamnet börjar som förväntat
                if filename.startswith(test_case['expected_prefix']):
                    print("✅ Filnamnsformat korrekt")
                else:
                    print(f"⚠️  Oväntat format. Förväntade prefix: {test_case['expected_prefix']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fel under test: {e}")
        return False

if __name__ == "__main__":
    success = test_filename_with_practice_name()
    if success:
        print("\n🎉 Filnamnstest genomfört!")
        print("🔍 Kontrollera output-mapparna för att se de genererade filnamnen")
    else:
        print("\n💥 Test misslyckades")
    
    input("\nTryck Enter för att avsluta...")