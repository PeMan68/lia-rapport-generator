"""
Anonymisering av Excel-fil för LIA-rapporter
Ersätter känslig information med generiska namn och företag
"""

import pandas as pd
import random
from datetime import datetime, timedelta

class ExcelAnonymizer:
    """Klass för att anonymisera känslig data i Excel-filer"""
    
    def __init__(self):
        # Generiska studentnamn
        self.student_names = [
            "Anna Andersson", "Erik Eriksson", "Maria Petersson", "Johan Johansson",
            "Lisa Larsson", "Michael Nilsson", "Sara Svensson", "David Gustafsson",
            "Emma Persson", "Alexander Olsson", "Hanna Lindberg", "Viktor Lindström"
        ]
        
        # Generiska företag
        self.companies = [
            "Teknik AB", "Industri Nord AB", "ElektroTech Sverige AB", 
            "Automation Solutions AB", "Nordic Engineering AB", "PowerTech AB",
            "Industrial Systems AB", "ElectroNord AB", "TechSolutions Sverige AB",
            "Engineering Partner AB", "ElTech Industries AB"
        ]
        
        # Generiska handledare
        self.supervisors = [
            "Lars Larsson", "Ann-Marie Svensson", "Mikael Andersson", "Christina Nilsson",
            "Per Johansson", "Helena Gustafsson", "Magnus Persson", "Birgitta Olsson",
            "Stefan Lindberg", "Margareta Lindström", "Patrik Holm"
        ]
    
    def anonymize_excel(self, input_file: str, output_file: str):
        """
        Anonymiserar Excel-fil och sparar som ny fil
        
        Args:
            input_file (str): Sökväg till original Excel-fil
            output_file (str): Sökväg till anonymiserad fil
        """
        print(f"📂 Läser Excel-fil: {input_file}")
        df = pd.read_excel(input_file)
        
        print(f"📊 Antal rader innan anonymisering: {len(df)}")
        
        # Randomisera ordningen på namnen
        random.shuffle(self.student_names)
        random.shuffle(self.companies)
        random.shuffle(self.supervisors)
        
        # Anonymisera studentnamn
        for i, row_idx in enumerate(df.index):
            if i < len(self.student_names):
                df.at[row_idx, 'Q1: Namn Yh-studerande'] = self.student_names[i]
            else:
                df.at[row_idx, 'Q1: Namn Yh-studerande'] = f"Student {i+1}"
        
        # Anonymisera företag
        for i, row_idx in enumerate(df.index):
            if i < len(self.companies):
                df.at[row_idx, 'Q2: Namn företag'] = self.companies[i]
            else:
                df.at[row_idx, 'Q2: Namn företag'] = f"Företag {i+1} AB"
        
        # Anonymisera handledare
        for i, row_idx in enumerate(df.index):
            if i < len(self.supervisors):
                df.at[row_idx, 'Q3: Namn handledare'] = self.supervisors[i]
            else:
                df.at[row_idx, 'Q3: Namn handledare'] = f"Handledare {i+1}"
        
        # Anonymisera datumstämplar (behåll samma tidsperiod men ändra exakta tider)
        if 'Inlämnad' in df.columns:
            base_date = datetime(2025, 5, 28, 7, 0, 0)  # Basera på original tidsperiod
            for i, row_idx in enumerate(df.index):
                # Lägg till slumpmässiga timmar inom samma dag
                random_hours = random.randint(0, 10)
                random_minutes = random.randint(0, 59)
                new_date = base_date + timedelta(hours=random_hours, minutes=random_minutes)
                df.at[row_idx, 'Inlämnad'] = new_date
        
        # Generalisera närvarotimmar (behåll strukturen men ta bort specifika detaljer)
        if 'Q4: Närvarotimmar vid företaget' in df.columns:
            generic_attendance = [
                "Full tid", "Cirka 200 timmar", "Normal arbetstid",
                "Enligt överenskommelse", "Fullständig närvaro",
                "Standard praktiktid", "Enligt schema"
            ]
            
            for i, row_idx in enumerate(df.index):
                df.at[row_idx, 'Q4: Närvarotimmar vid företaget'] = generic_attendance[i % len(generic_attendance)]
        
        # Generalisera kommentarer (ta bort för specifika referenser)
        comment_columns = [col for col in df.columns if 'Kommentar' in col]
        
        for col in comment_columns:
            for row_idx in df.index:
                original_comment = df.at[row_idx, col]
                if pd.notna(original_comment) and str(original_comment).strip():
                    # Ersätt med generisk kommentar baserat på typ
                    generic_comment = self._generalize_comment(str(original_comment))
                    df.at[row_idx, col] = generic_comment
        
        # Spara anonymiserad fil
        df.to_excel(output_file, index=False)
        print(f"✅ Anonymiserad fil sparad: {output_file}")
        print(f"📊 Antal rader efter anonymisering: {len(df)}")
        
        return True
    
    def _generalize_comment(self, comment: str) -> str:
        """
        Generaliserar kommentarer för att ta bort specifika referenser
        
        Args:
            comment (str): Original kommentar
            
        Returns:
            str: Generaliserad kommentar
        """
        comment_lower = comment.lower()
        
        # Positive kommentarer
        if any(word in comment_lower for word in ['mycket bra', 'utmärkt', 'fantastisk', 'excellent']):
            return "Mycket positiva resultat och bra prestationer."
        
        if any(word in comment_lower for word in ['bra', 'bra', 'good', 'positivt']):
            return "Bra resultat och utveckling."
        
        if any(word in comment_lower for word in ['intresserad', 'nyfiken', 'frågor']):
            return "Visar stort intresse och ställer relevanta frågor."
        
        if any(word in comment_lower for word in ['lära', 'utveckling', 'förståelse']):
            return "Bra inlärningsförmåga och utveckling under praktiken."
        
        if any(word in comment_lower for word in ['samarbete', 'social', 'teamwork']):
            return "Fungerar bra i team och visar god samarbetsförmåga."
        
        if any(word in comment_lower for word in ['säkerhet', 'risker', 'försiktig']):
            return "Medveten om säkerhetsaspekter och följer rutiner."
        
        if any(word in comment_lower for word in ['självständig', 'initiativ']):
            return "Visar självständighet och tar egna initiativ."
        
        # Neutral/developmental kommentarer
        if any(word in comment_lower for word in ['svårt att bedöma', 'kort tid']):
            return "Svårt att bedöma på grund av begränsad tid."
        
        if any(word in comment_lower for word in ['utveckla', 'förbättra', 'mer']):
            return "Finns utvecklingspotential inom området."
        
        # Fallback
        if len(comment.strip()) > 0:
            return "Kommentar från handledare tillgänglig."
        
        return ""


def main():
    """Huvudfunktion för anonymisering"""
    anonymizer = ExcelAnonymizer()
    
    # För framtida användning - lägg originalfil här
    input_file = "din_original_fil.xlsx"  # Användaren byter ut denna
    output_file = "data/exempel_data.xlsx"
    
    print("🔒 ANONYMISERING AV EXCEL-FIL")
    print("=" * 40)
    print("⚠️  VIKTIGT: Detta ersätter känslig information med generiska värden")
    print("📋 Original fil behålls oförändrad")
    print(f"📁 Lägg din originalfil som: {input_file}")
    print()
    
    # Kontrollera om filen finns
    import os
    if not os.path.exists(input_file):
        print(f"❌ Filen '{input_file}' hittades inte")
        print("📝 För att använda anonymiseringen:")
        print("   1. Lägg din Excel-fil i projektmappen")
        print("   2. Byt namn till 'din_original_fil.xlsx' ELLER")
        print("   3. Ändra 'input_file' variabeln i main() funktionen")
        return
    
    try:
        anonymizer.anonymize_excel(input_file, output_file)
        print("\n✅ Anonymisering slutförd!")
        print(f"📁 Anonymiserad fil: {output_file}")
        print("🔒 Nu säker att dela eller committa till git")
        
    except Exception as e:
        print(f"❌ Fel vid anonymisering: {e}")


if __name__ == "__main__":
    main()