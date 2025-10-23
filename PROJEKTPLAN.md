# 📋 PROJEKTPLAN: Excel till PDF-rapporter

## 🎯 Projektmål
Skapa ett Python-verktyg som konverterar Excel-fil med studentomdömen till individuella PDF-rapporter. Verktyget ska kunna användas av alla lärare i Windows/Office-miljö.

## 🛠️ Teknisk Stack
- **Språk:** Python 3.13
- **Excel-hantering:** pandas, openpyxl
- **PDF-generering:** reportlab
- **GUI:** tkinter (inbyggt)
- **Distribution:** PyInstaller (.exe)
- **Versionshantering:** Git med Git Flow

---

## 📅 PROJEKTFASER

### **Fas 1: Projektuppsättning** 
- [x] 🔄 Skapa Git-repo med Git Flow
- [x] 📦 Installera nödvändiga Python-paket
- [x] 📁 Skapa projektstruktur
- [x] 📝 Dokumentera Excel-filstruktur

### **Fas 2: Kärnfunktionalitet**
- [x] 📊 Excel-läsare (parsing av studentdata)
- [ ] 🎨 PDF-rapportmall (design och layout)
- [ ] 🔄 PDF-generator (en rapport per student)
- [ ] ✅ Testa med befintlig Excel-fil

### **Fas 3: Användargränssnitt**
- [ ] 🖥️ GUI för filval (Excel-fil)
- [ ] 📂 GUI för utdatamapp
- [ ] ⚙️ Inställningar och konfiguration
- [ ] 🔄 Progress bar för generering

### **Fas 4: Robusthet & Felhantering**
- [ ] 🛡️ Validering av Excel-filformat
- [ ] ❌ Felhantering och användarmeddelanden
- [ ] 📊 Logging och felsökning
- [ ] 🧪 Enhetstester

### **Fas 5: Optimering & Rensning**
- [ ] 🧹 Ta bort utvecklingsscript (analyze_excel.py, anonymize_data.py)
- [ ] 📁 Organisera projektstruktur för distribution
- [ ] 📝 Uppdatera dokumentation för slutanvändare
- [ ] 🔍 Kod-granskning och refaktorering
- [ ] 🗑️ Ta bort data/exempel_data.xlsx (användare ska välja egen fil)

### **Fas 6: Distribution**
- [ ] 📦 PyInstaller-konfiguration
- [ ] 🎯 Skapa .exe-fil
- [ ] 📖 Användarmanual för kollegor
- [ ] 🚀 Installation och deployment

---

## 📂 PROJEKTSTRUKTUR
```
RapportFrån LIA/
├── src/
│   ├── excel_reader.py      # Excel-filhantering
│   ├── pdf_generator.py     # PDF-skapande
│   ├── gui.py              # Användargränssnitt
│   └── main.py             # Huvudapplikation
├── templates/
│   └── rapport_mall.py     # PDF-rapportmall
├── tests/
│   └── test_*.py           # Enhetstester
├── docs/
│   └── användarmanual.md   # Dokumentation
├── data/
│   └── exempel_data.xlsx   # Testdata
├── output/                 # Genererade rapporter
├── requirements.txt        # Python-dependencies
├── build_exe.py           # PyInstaller-script
└── README.md              # Projektbeskrivning
```

---

## 🔄 GIT FLOW BRANCHES
- **main:** Stabil produktionskod
- **develop:** Utvecklingsbranch
- **feature/*:** Nya funktioner
- **release/*:** Release-förberedelser
- **hotfix/*:** Snabba bugfixar

---

## ✅ FRAMSTEG

### 🟢 Klart
- [x] Analyserat Excel-filstruktur (11 studenter, 36 kolumner)
- [x] Identifierat bedömningsområden (14 st)
- [x] Valt teknisk stack (Python/reportlab)
- [x] Git-repo uppsättning med Git Flow
- [x] Excel-läsare implementation (LIAExcelReader)
- [x] Projektstruktur skapad
- [x] Requirements.txt med dependencies

### 🟡 Pågående
- [ ] PDF-rapportmall design

### 🔴 Att göra
- [ ] Alla andra punkter enligt plan

---

## 📊 MILSTOLPAR
1. **V1.0 - MVP:** Grundläggande Excel → PDF (1 vecka)
2. **V1.1 - GUI:** Användarvänligt gränssnitt (3 dagar)
3. **V1.2 - POLISH:** Optimering och rensning (1 dag)
4. **V1.3 - EXE:** Distribuerbar .exe-fil (2 dagar)
5. **V1.4 - PROD:** Färdig för kollegor (1 dag)

---

## 🎯 ACCEPTANSKRITERIER
- [ ] Läser Excel-fil korrekt
- [ ] Genererar en PDF per student
- [ ] Professionell rapportlayout
- [ ] Hanterar svenska tecken
- [ ] Enkelt GUI för lärare
- [ ] .exe-fil som fungerar utan Python-installation
- [ ] Användarmanual för kollegor

---

*Senast uppdaterad: 2025-10-23*