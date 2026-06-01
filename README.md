# 🎓 LIA Rapportgenerator

**Version 1.1.0** - Produktionsklar automatisk generator för individuella PDF-rapporter från Excel-fil med LIA-bedömningar.

## 📋 Beskrivning
Automatisk generator för individuella PDF-rapporter från Excel-fil med LIA-bedömningar. Skapar professionella rapporter för varje student baserat på praktikbedömningar. **Anpassar sig automatiskt till olika Excel-format** med liknande struktur.

## ✨ Funktioner
- 📊 **Flexibel Excel-läsning**: Anpassar sig automatiskt till olika filformat och antal bedömningsområden
- 📄 Genererar individuella PDF-rapporter per student
- 🎨 Professionell layout med strukturerade sektioner
- 🖥️ Användarvänligt grafiskt gränssnitt
- 🏢 Anpassningsbara praktiknamn och period i rapporter
- 🔍 **Selektiv kommentarsgranskning**: granska och dölj enstaka kommentarer per student innan PDF-generering
- ✅ **Automatisk strukturvalidering**: Identifierar kolumner och bedömningsområden automatiskt
- 📁 **Intelligent filnamning**: Inkluderar praktiknamn för enkel identifiering
- 🔧 **Stödjer olika Q-frågeformat**: Fungerar med Q1-Q30, Q1-Q34, och andra varianter

## 🚀 Komma igång

### 🎯 **För lärare (Enklaste metoden)**
1. **Ladda ner** `LIA_Rapportgenerator.exe` från release
2. **Dubbelklicka** på exe-filen för att starta
3. **Färdig!** - Inga installationer behövs

### 💾 **För utvecklare (Python-källkod)**
1. Ladda ner projektet
2. Öppna terminal/kommandotolken i projektmappen
3. Installera beroenden:
   ```bash
   pip install -r requirements.txt
   ```

### ▶️ Starta applikationen
```bash
# Med exe-fil (lärare)
Dubbelklicka på LIA_Rapportgenerator.exe

# Med Python (utvecklare)
python main.py
```

### 📝 Användning
1. **Praktikinfo**: Ange praktiknamn och period för rapporterna
2. **Välj Excel-fil**: Klicka "Välj fil..." och välj din Excel-fil med LIA-bedömningar
   - ✅ Stödjer olika format (Q1-Q30, Q1-Q34, etc.)
   - ✅ Automatisk strukturidentifiering
3. **Välj utdatamapp**: Ange var PDF-rapporterna ska sparas
4. **Validera**: Klicka "Validera Excel-fil" för att kontrollera innehållet
5. **Granska** *(valfritt)*: Klicka "Granska kommentarer" för att dölja enstaka kommentarer i studentversionen
6. **Generera**: Klicka "Generera alla rapporter" för att skapa PDF:er

## 📊 Excel-filformat

### 🔧 Flexibelt strukturstöd
Applikationen anpassar sig automatiskt till olika Excel-format med liknande struktur:

### Obligatoriska kolumner (identifieras automatiskt):
- **Studentnamn**: Kolumner som innehåller "namn" + "studerande" eller "student"
- **Företag**: Kolumner som innehåller "företag" eller "company"
- **Handledare**: Kolumner som innehåller "handledare" eller "supervisor"
- **Närvarotid**: Kolumner som innehåller "närvarotimmar" eller "närvaro"
- **Slutbetyg**: Kolumner som innehåller "helhetsintryck" eller "slutbetyg"
- **Slutkommentarer**: Kolumner som slutar med "kommentarer"

### Bedömningsområden:
- **Flexibelt Q-format**: Stödjer Q1-Q30, Q1-Q34, Q1-Q40, etc.
- **Automatisk identifiering**: Hittar bedömningsområden och tillhörande kommentarer automatiskt
- **Varierande antal**: Anpassar sig till olika antal bedömningsområden per fil

### Exempel på stödda format:
- **Format 1**: Q1-Q34 (14 bedömningsområden) - Webbutveckling
- **Format 2**: Q1-Q30 (12 bedömningsområden) - Processteknik
- **Format 3**: Andra varianter med liknande struktur

**Betygsskala**: "3 Mycket bra", "2 Bra", "1 Bör förbättras"

## 📄 PDF-rapportstruktur

### 🏢 Praktikplats
- Student, företag, handledare, närvarotid

### 📊 Bedömning
- Olika antal bedömningsområden med betyg och kommentarer, t. ex.:
  - Arbetets kvalitet
  - Arbetstider
  - Kreativitet
  - Intresse för arbetet
  - Initiativförmåga
  - Samarbetsförmåga

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
│   ├── excel_reader.py      # Excel-filhantering
│   ├── pdf_generator.py     # PDF-generering
│   ├── gui.py               # Grafiskt gränssnitt
│   └── comment_filter.py    # Kommentarsgranskningsdialog
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
- **v1.1.0** - Selektiv kommentarsgranskning
- **v1.0.1** - Buggfixar
- **v1.0.0** - Första stabila version

---
*Skapad för att förenkla LIA-rapportering för lärare och handledare*
