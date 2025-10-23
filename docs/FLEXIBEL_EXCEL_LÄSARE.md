# 🔧 Flexibel Excel-läsare - Teknisk dokumentation

## 🎯 Översikt
Den flexibla Excel-läsaren (`FlexibleLIAExcelReader`) är en intelligent komponent som automatiskt anpassar sig till olika Excel-format med liknande struktur. Den ersätter den ursprungliga fasta läsaren och gör applikationen kompatibel med olika källor av LIA-bedömningsdata.

## ✨ Huvudfunktioner

### 🔍 Automatisk strukturidentifiering
- **Regex-baserad kolonnsökning**: Hittar kolumner baserat på innehållsmönster istället för exakta namn
- **Flexibel Q-frågehantering**: Anpassar sig till olika antal Q-frågor (Q1-Q30, Q1-Q34, etc.)
- **Intelligent bedömningsgruppering**: Identifierar bedömningsområden och tillhörande kommentarer automatiskt

### 📊 Stödda format

#### **Format 1: Webbutveckling** (`exempel_data.xlsx`)
- **Studenter**: 11
- **Q-frågor**: Q1-Q34
- **Bedömningsområden**: 14 (Q5-Q32)
- **Slutbetyg**: Q33 "Helhetsintryck"
- **Slutkommentarer**: Q34 "Kommentarer"

#### **Format 2: Processteknik** (`results_for_survey_586559445.xlsx`)
- **Studenter**: 18
- **Q-frågor**: Q1-Q30
- **Bedömningsområden**: 12 (Q5-Q28)
- **Slutbetyg**: Q29 "Helhetsintryck"
- **Slutkommentarer**: Q30 "Kommentarer"

## 🛠️ Teknisk implementation

### Klasser och metoder

```python
class FlexibleLIAExcelReader:
    def auto_detect_structure(self) -> bool
    def _identify_basic_columns(self)
    def _identify_assessment_areas(self)
    def _identify_final_sections(self)
    def extract_student_data(self) -> bool
```

### Identifieringsmönster

#### Grundkolumner
- **Studentnamn**: `['namn.*studerande', 'student.*namn', r'q\d+.*namn.*studerande']`
- **Företag**: `['namn.*företag', 'företag.*namn', r'q\d+.*företag']`
- **Handledare**: `['namn.*handledare', 'handledare.*namn', r'q\d+.*handledare']`
- **Närvarotid**: `['närvarotimmar', 'närvaro.*tid', r'q\d+.*närvarotimmar']`

#### Slutsektioner
- **Slutbetyg**: `['helhetsintryck', 'slutbetyg', 'total.*betyg', 'övergripande']`
- **Slutkommentarer**: `['kommentarer$', 'slutkommentar', 'avslutande.*kommentar']`

## 🔄 Arbetsflöde

1. **Laddning**: Excel-fil läses in med pandas
2. **Strukturanalys**: Kolumner analyseras och mappas automatiskt
3. **Bedömningsidentifiering**: Q-frågor grupperas i bedömningsområden
4. **Dataextraktion**: Studentdata extraheras enligt identifierad struktur
5. **Validering**: Kontrollerar att nödvändig data hittats

## 📈 Fördelar

### För användare
- ✅ **Plug-and-play**: Fungerar direkt med olika Excel-format
- ✅ **Ingen konfiguration**: Automatisk anpassning
- ✅ **Tydliga felmeddelanden**: Om strukturen inte kan identifieras

### För utvecklare
- ✅ **Framtidssäker**: Nya format kan hanteras utan kodändringar
- ✅ **Robust**: Hantera variationer i kolumnnamn och ordning
- ✅ **Utbyggbar**: Enkelt att lägga till nya identifieringsmönster

## 🧪 Testning

### Automatiska tester
- `test_flexible_reader.py`: Testar båda format-typerna
- Validerar strukturidentifiering och dataextraktion
- Kontrollerar kompatibilitet med befintlig PDF-generering

### Manuell testning
- GUI-testning med olika Excel-filer
- Validering av genererade PDF-rapporter
- Kontroll av felhantering vid ogiltiga filer

## 🔮 Framtida utveckling

### Möjliga förbättringar
- **Konfigurerbar mappning**: Tillåta användare att justera kolumnmappning
- **Format-detektering**: Automatisk identifiering av filtyp och anpassning
- **Batch-validering**: Validera flera filer samtidigt
- **Template-stöd**: Stöd för helt andra bedömningstyper (inte bara LIA)

### Nya format som kan stödjas
- Andra utbildningsprogram med liknande struktur
- Internationella format med översättningar
- Äldre Excel-versioner med något annorlunda layout

## 📋 Underhåll

### Vanliga problem
- **Kolumn inte hittad**: Lägg till nytt regex-mönster i identifieringslistan
- **Fel antal bedömningsområden**: Kontrollera skip-patterns för slutsektioner
- **Datafel**: Validera att cellvärden extraheras korrekt

### Felsökning
- Aktivera debug-logging för detaljerad strukturanalys
- Använd `get_structure_summary()` för att inspektera identifierad struktur
- Testa med `analyze_new_excel.py` för att förstå nya format