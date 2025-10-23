# 📊 Data-mapp

## 📋 Beskrivning
Denna mapp innehåller exempel-data för utveckling och testning av PDF-rapportgeneratorn. Applikationen stödjer nu **flexibla Excel-format** och anpassar sig automatiskt till olika strukturer.

## 📁 Filer

### `exempel_data.xlsx` - Webbutveckling Format
- **Anonymiserad** Excel-fil för utveckling
- **Studenter**: 11
- **Bedömningsområden**: 14 (Q5-Q32)
- **Slutbetyg**: Q33 "Helhetsintryck"
- **Fokus**: Webbutveckling och digitala färdigheter
- Baserad på verkligt LIA-data men med:
  - Generiska studentnamn
  - Generiska företagsnamn  
  - Generiska handledarnamn
  - Generaliserade kommentarer
- **Säker att dela** och committa till git

### `results_for_survey_586559445.xlsx` - Processteknik Format  
- **Verklig data** för testning
- **Studenter**: 18
- **Bedömningsområden**: 12 (Q5-Q28)
- **Slutbetyg**: Q29 "Helhetsintryck"
- **Fokus**: Processteknisk tillverkning och automation

## 🔧 Automatisk formatidentifiering

Applikationen identifierar automatiskt:
- ✅ Antal studenter och bedömningsområden
- ✅ Kolumnstruktur och Q-frågor
- ✅ Slutbetyg och kommentarsektioner
- ✅ Grundläggande information (namn, företag, handledare)

## ⚠️ Viktigt för utvecklare

### Känsliga filer (EJ i git):
- `results_for_survey_*.xlsx` - Verklig data
- `*_original.xlsx` - Original filer
- `*_real_data.xlsx` - Känslig data

### Vid testning:
1. **Under utveckling:** Använd `exempel_data.xlsx`
2. **Vid release:** Användare väljer egen fil via GUI
3. **Aldrig committa** verklig data till git

## 🔄 Anonymisering
För att skapa ny testdata:
```bash
python anonymize_data.py
```

## 📝 Excel-struktur
Förväntad struktur för Excel-filer:
- `Q1: Namn Yh-studerande` - Studentnamn
- `Q2: Namn företag` - Företagsnamn  
- `Q3: Namn handledare` - Handledarnamn
- `Q4: Närvarotimmar vid företaget` - Närvarotid
- `Q5-Q32: Bedömningar` - 14 bedömningsområden med betyg och kommentarer
- `Q33: Helhetsintryck` - Slutbetyg
- `Q34: Kommentarer` - Avslutande kommentarer