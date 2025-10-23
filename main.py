"""
LIA Rapportgenerator - Huvudapplikation
Skapar individuella PDF-rapporter från Excel-fil med LIA-bedömningar
"""

import sys
import os
from pathlib import Path

# Lägg till projektets rotkatalog till Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Importera GUI
from src.gui import main as start_gui

def main():
    """Huvudfunktion som startar applikationen"""
    print("🚀 Startar LIA Rapportgenerator...")
    
    # Kontrollera att nödvändiga moduler finns
    try:
        import pandas
        import openpyxl
        import reportlab
        print("✅ Alla nödvändiga bibliotek installerade")
    except ImportError as e:
        print(f"❌ Saknas bibliotek: {e}")
        print("\nInstallera med: pip install -r requirements.txt")
        input("Tryck Enter för att avsluta...")
        return
    
    # Skapa output-mapp om den inte finns
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)
    
    print("✅ Projektstruktur kontrollerad")
    print("🖥️  Startar GUI...")
    
    # Starta GUI
    try:
        start_gui()
    except KeyboardInterrupt:
        print("\n👋 Applikation avslutad av användare")
    except Exception as e:
        print(f"❌ Fel vid start av applikation: {e}")
        input("Tryck Enter för att avsluta...")


if __name__ == "__main__":
    main()