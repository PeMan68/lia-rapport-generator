#!/usr/bin/env python3
"""
Analyserar ny Excel-fil för att förstå strukturen och skillnader
"""

import pandas as pd
import sys
import os

def analyze_new_excel_file():
    """Analyserar den nya Excel-filen"""
    file_path = "data/results_for_survey_586559445.xlsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Fil hittades inte: {file_path}")
        return
    
    try:
        print(f"📊 Analyserar: {file_path}")
        print("=" * 50)
        
        # Läs Excel-fil
        df = pd.read_excel(file_path)
        
        print(f"📝 Antal rader: {len(df)}")
        print(f"📋 Antal kolumner: {len(df.columns)}")
        print()
        
        print("🔤 KOLUMNNAMN:")
        print("-" * 30)
        for i, col in enumerate(df.columns, 1):
            print(f"{i:2d}. {col}")
        print()
        
        # Jämför med förväntat format
        print("🔍 STRUKTURANALYS:")
        print("-" * 30)
        
        # Leta efter namnkolumn
        name_cols = [col for col in df.columns if any(word in col.lower() for word in ['namn', 'name', 'student'])]
        print(f"Möjliga namnkolumner: {name_cols}")
        
        # Leta efter företagskolumn
        company_cols = [col for col in df.columns if any(word in col.lower() for word in ['företag', 'company', 'arbetsplats'])]
        print(f"Möjliga företagskolumner: {company_cols}")
        
        # Leta efter Q-frågor
        q_cols = [col for col in df.columns if col.startswith('Q')]
        print(f"Q-frågor (antal): {len(q_cols)}")
        print(f"Q-intervall: Q{min([int(col.split(':')[0][1:]) for col in q_cols if ':' in col])} - Q{max([int(col.split(':')[0][1:]) for col in q_cols if ':' in col])}")
        
        print()
        print("📋 FÖRSTA RADEN (data):")
        print("-" * 30)
        if len(df) > 0:
            first_row = df.iloc[0]
            for col in df.columns[:10]:  # Visa första 10 kolumnerna
                value = first_row[col]
                if pd.notna(value):
                    print(f"{col}: {value}")
        
        print()
        print("🔤 Q-FRÅGOR I DETALJ:")
        print("-" * 30)
        for col in sorted(q_cols)[:20]:  # Visa första 20 Q-frågorna
            print(f"{col}")
            
    except Exception as e:
        print(f"❌ Fel vid analys: {e}")

if __name__ == "__main__":
    analyze_new_excel_file()
    input("\nTryck Enter för att fortsätta...")