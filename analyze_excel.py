import pandas as pd
import sys

def analyze_excel_file(file_path):
    """Analyserar Excel-fil och visar struktur och innehåll"""
    
    try:
        # Läs Excel-filen
        print(f"Analyserar Excel-fil: {file_path}")
        print("=" * 50)
        
        # Läs först några rader för att se strukturen
        df = pd.read_excel(file_path)
        
        print(f"Antal rader: {len(df)}")
        print(f"Antal kolumner: {len(df.columns)}")
        print("\nKolumnnamn:")
        for i, col in enumerate(df.columns, 1):
            print(f"{i:2d}. {col}")
        
        print("\n" + "=" * 50)
        print("FÖRSTA 3 RADERNA:")
        print("=" * 50)
        print(df.head(3).to_string())
        
        print("\n" + "=" * 50)
        print("DATATYPER:")
        print("=" * 50)
        print(df.dtypes)
        
        print("\n" + "=" * 50)
        print("STATISTIK FÖR NUMERISKA KOLUMNER:")
        print("=" * 50)
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            print(df[numeric_cols].describe())
        else:
            print("Inga numeriska kolumner hittades")
        
        print("\n" + "=" * 50)
        print("UNIKA VÄRDEN I VARJE KOLUMN (max 10 per kolumn):")
        print("=" * 50)
        for col in df.columns:
            unique_vals = df[col].unique()
            print(f"\n{col}:")
            if len(unique_vals) <= 10:
                for val in unique_vals:
                    if pd.notna(val):
                        print(f"  - {val}")
            else:
                print(f"  - {len(unique_vals)} unika värden")
                print(f"  - Exempel: {list(unique_vals[:5])}")
        
        # Kontrollera om det finns tomma celler
        print("\n" + "=" * 50)
        print("TOMMA CELLER:")
        print("=" * 50)
        missing_data = df.isnull().sum()
        for col, missing_count in missing_data.items():
            if missing_count > 0:
                print(f"{col}: {missing_count} tomma celler")
        
        if missing_data.sum() == 0:
            print("Inga tomma celler hittades")
            
    except Exception as e:
        print(f"Fel vid analys av Excel-filen: {e}")
        return False
    
    return True

if __name__ == "__main__":
    file_path = "results_for_survey_596702594.xlsx"
    analyze_excel_file(file_path)