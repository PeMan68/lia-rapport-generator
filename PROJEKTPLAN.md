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
- [ ] 📦 Installera nödvändiga Python-paket
- [ ] 📁 Skapa projektstruktur
- [ ] 📝 Dokumentera Excel-filstruktur

### **Fas 2: Kärnfunktionalitet**
- [ ] 📊 Excel-läsare (parsing av studentdata)
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

### **Fas 5: Distribution**
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

### 🟡 Pågående
- [ ] Excel-läsare implementation (feature/excel-reader)

### 🔴 Att göra
- [ ] Alla andra punkter enligt plan

---

## 📊 MILSTOLPAR
1. **V1.0 - MVP:** Grundläggande Excel → PDF (1 vecka)
2. **V1.1 - GUI:** Användarvänligt gränssnitt (3 dagar)
3. **V1.2 - EXE:** Distribuerbar .exe-fil (2 dagar)
4. **V1.3 - PROD:** Färdig för kollegor (1 dag)

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