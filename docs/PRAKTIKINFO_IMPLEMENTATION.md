# Implementering av Praktikinfo-funktioner

## 🎯 Mål
Lägg till möjlighet att ange praktiknamn och period i GUI:n och inkludera denna information i PDF-rapporterna.

## ✅ Genomförda förändringar

### 1. GUI-uppdateringar (`src/gui.py`)
- Lagt till två nya StringVar-variabler:
  - `self.practice_name` (standard: "LIA-praktik")  
  - `self.practice_period` (standard: "VT 2024")
- Uppdaterat GUI-layouten med ny sektion "Praktikinfo":
  - Inmatningsfält för praktiknamn
  - Inmatningsfält för period
- Modifierat `_generate_reports_thread()` för att skicka praktikuppgifter till PDF-generatorn

### 2. PDF-generator uppdateringar (`src/pdf_generator.py`)
- Uppdaterat `generate_all_reports()` metoden för att acceptera:
  - `practice_name` parameter
  - `practice_period` parameter
- Skickar praktikinfo vidare till PDF-mallen

### 3. PDF-mall förbättringar (`templates/rapport_mall.py`)
- Uppdaterat `create_report()` för att ta emot praktikparametrar
- Modifierat huvudrubriken för att inkludera:
  - Praktiknamn (om angivet)
  - Period (om angiven)
- Uppdaterat `_create_basic_info_section()` för att lägga till praktikinfo i grundinformationstabellen

## 🧪 Testresultat
- Skapat `test_practice_info.py` för automatisk validering
- Framgångsrikt genererat 11 test-rapporter med praktikinfo:
  - Praktiknamn: "Webbutveckling vårterminen"
  - Period: "2024-03-01 till 2024-05-31"
- Alla PDF-filer skapades utan fel i `output/test_practice_info/`

## 🔄 Användarflöde
1. Användaren startar applikationen (`python main.py`)
2. I GUI:n anger användaren:
   - Praktiknamn (ex: "Webbutveckling vårterminen")
   - Period (ex: "VT 2024")
3. Väljer Excel-fil med LIA-data
4. Klickar "Generera alla rapporter"
5. PDF-rapporterna genereras med praktikinfo i:
   - Huvudrubrik på första sidan
   - Grundinformationstabellen

## 📋 Tekniska detaljer
- **Bakåtkompatibilitet**: Funktionen är helt bakåtkompatibel - om inga praktikuppgifter anges används standardvärden
- **Felhantering**: Robust felhantering om praktikfält lämnas tomma
- **Kodkvalitet**: Inga brytande förändringar i befintlig funktionalitet

## 🎉 Resultat
Användare kan nu skapa mer professionella och specifika LIA-rapporter med tydlig identifiering av praktiknamn och period direkt från GUI:n.