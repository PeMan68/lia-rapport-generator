# 🎓 LIA Rapportgenerator

## 📋 Beskrivning
Automatisk generator för individuella PDF-rapporter från Excel-fil med LIA-bedömningar. Skapar professionella rapporter för varje student baserat på praktikbedömningar.

## ✨ Funktioner
- 📊 Läser Excel-filer med LIA-bedömningar
- 📄 Genererar individuella PDF-rapporter per student
- 🎨 Professionell layout med strukturerade sektioner
- 🖥️ Användarvänligt grafiskt gränssnitt
- ✅ Validering av Excel-filstruktur
- 📁 Automatisk filorganisering med säkra filnamn

## 🚀 Komma igång

### 💾 Installation
1. Ladda ner projektet
2. Öppna terminal/kommandotolken i projektmappen
3. Installera beroenden:
   ```bash
   pip install -r requirements.txt
   ```

### ▶️ Starta applikationen
```bash
python main.py
```

### 📝 Användning
1. **Välj Excel-fil**: Klicka "Välj fil..." och välj din Excel-fil med LIA-bedömningar
2. **Välj utdatamapp**: Ange var PDF-rapporterna ska sparas
3. **Validera**: Klicka "Validera Excel-fil" för att kontrollera innehållet
4. **Generera**: Klicka "Generera alla rapporter" för att skapa PDF:er

## 📊 Excel-filformat

### Obligatoriska kolumner:
- `Q1: Namn Yh-studerande` - Studentens namn
- `Q2: Namn företag` - Företagsnamn
- `Q3: Namn handledare` - Handledarens namn
- `Q4: Närvarotimmar vid företaget` - Närvarotid
- `Q33: Helhetsintryck` - Slutbetyg
- `Q34: Kommentarer` - Avslutande kommentarer

### Bedömningsområden (Q5-Q32):
Varje bedömningsområde har två kolumner:
- Betyg (t.ex. "Q5: Arbetets kvalitet...")
- Kommentar (t.ex. "Q6: Kommentar")

**Betygsskala**: "3 Mycket bra", "2 Bra", "1 Bör förbättras"

## 📄 PDF-rapportstruktur

### 🏢 Praktikplats
- Student, företag, handledare, närvarotid

### 📊 Bedömning
- 14 bedömningsområden med betyg och kommentarer:
  - Arbetets kvalitet
  - Arbetstider
  - Kreativitet
  - Intresse för arbetet
  - Initiativförmåga
  - Samarbetsförmåga
  - Kunskap om risker
  - Eldistribution
  - Dokumentation
  - Problemredogörelse
  - Felsökning
  - Säkerhetskunskap
  - Installation och drift
  - Förebyggande underhåll

### 🎯 Sammanfattning
- Helhetsintryck
- Avslutande kommentarer
- Betygsstatistik

## 🔧 Teknisk information

### Systemkrav
- Windows 10/11
- Python 3.8+ (för utvecklare)

### Beroenden
- `pandas` - Excel-filhantering
- `openpyxl` - Excel-läsning
- `reportlab` - PDF-generering
- `tkinter` - GUI (ingår i Python)

### Projektstruktur
```
LIA-Rapportgenerator/
├── main.py              # Huvudapplikation
├── src/
│   ├── excel_reader.py  # Excel-filhantering
│   ├── pdf_generator.py # PDF-generering
│   └── gui.py          # Grafiskt gränssnitt
├── templates/
│   └── rapport_mall.py  # PDF-rapportmall
├── output/             # Genererade PDF:er
├── requirements.txt    # Python-beroenden
└── README.md          # Denna fil
```

## ❓ Felsökning

### "Excel-fil ogiltig"
- Kontrollera att filen har rätt kolumnnamn
- Se till att det finns studentdata (inte bara rubriker)
- Kontrollera att betyg följer formatet "3 Mycket bra", "2 Bra", etc.

### "Kunde inte skapa rapport"
- Kontrollera att utdatamappen är skrivbar
- Se till att PDF-filer inte är öppna i andra program
- Kontrollera att det finns diskutrymme

### Import-fel
- Kör `pip install -r requirements.txt`
- Kontrollera att Python-versionen är 3.8 eller senare

## 👥 För utvecklare

### Git Flow
- `main`: Stabil produktionskod
- `develop`: Utvecklingsbranch  
- `feature/*`: Nya funktioner

### Testning
```bash
# Testa Excel-läsare
cd src
python excel_reader.py

# Testa PDF-generator
python pdf_generator.py

# Testa GUI
python gui.py
```

## 📄 Licens
Detta projekt är skapat för utbildningsändamål.

## 🆔 Version
v1.0 - Första stabila version

---
*Skapad för att förenkla LIA-rapportering för lärare och handledare*