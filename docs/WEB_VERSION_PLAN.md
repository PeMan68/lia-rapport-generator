# 🌐 Web-version Plan - LIA Rapportgenerator

## 📋 Översikt
Plan för att konvertera desktop-applikationen till en web-baserad lösning med Pyodide (Python i webbläsaren). Helt frontend-baserad utan behov av server.

**Utvecklingstid**: 9 timmar (baserat på att v1.0.1 desktop tog 3h)  
**Hosting-kostnad**: 0 SEK/månad (GitHub Pages)  
**Målgrupp**: Lärare på alla plattformar (Windows, Mac, Linux, mobil)

---

## 🎯 **Fördelar med web-version**

### **För lärare:**
- ✅ **Plattformsoberoende** - Fungerar på Mac, Linux, Chromebook
- ✅ **Mobilvänlig** - Kan användas på surfplattor
- ✅ **Inget att installera** - Bara öppna länk i webbläsare
- ✅ **Automatiska uppdateringar** - Alltid senaste version
- ✅ **Offline-funktionalitet** - Fungerar utan internet efter första laddning
- ✅ **PWA-installation** - Kan installeras som "app" på telefon/dator

### **För IT-avdelningar:**
- ✅ **Ingen installation** på användardatorer
- ✅ **Centraliserad hantering** - En URL för alla
- ✅ **Säkerhet** - Körs isolerat i webbläsare
- ✅ **Inga server-kostnader** - Helt statisk hosting

### **För utvecklare:**
- ✅ **Gratis hosting** (GitHub Pages/Netlify)
- ✅ **Automatisk deployment** från Git
- ✅ **Ingen server-administration**
- ✅ **Skalbart** - Hanterar många användare utan extra kostnad

---

## 🏗️ **Teknisk arkitektur**

### **Pyodide-baserad lösning**
```
Frontend (HTML/CSS/JavaScript)
├── File upload interface
├── Praktikinfo formulär
├── Progress indicators
└── PDF download

Pyodide Runtime (i webbläsare)
├── Python 3.11 runtime
├── pandas, openpyxl (Excel-hantering)
├── reportlab (PDF-generering) 
└── Befintlig Python-kod (70% återanvändning)

Hosting
├── GitHub Pages (gratis)
├── Netlify/Vercel (också gratis)
└── Egen domän (valfritt)
```

### **Repository-struktur**
```
lia-rapport-generator/
├── main branch (nuvarande desktop-app)
├── web-version branch (ny web-app)
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   ├── pyodide-worker.js
│   ├── src/ (Python-kod kopierad från main)
│   │   ├── flexible_excel_reader.py
│   │   ├── pdf_generator.py
│   │   └── rapport_mall.py
│   ├── manifest.json (PWA)
│   └── requirements.txt (Pyodide-paket)
└── docs/ (delad dokumentation)
```

---

## ⏱️ **Implementationsplan (9 timmar)**

### **Fas 1: Setup och grundstruktur (3h)**

#### **Timme 1: Git och hosting setup**
- Skapa `web-version` branch från `develop`
- Grundläggande HTML-struktur
- Setup GitHub Pages eller Netlify

#### **Timme 2: Pyodide integration**
- Ladda Pyodide runtime
- Installera Python-paket (pandas, openpyxl, reportlab)
- Testa grundläggande Python-exekvering i browser

#### **Timme 3: File upload**
- HTML file input för Excel-filer
- JavaScript för att läsa filer som ArrayBuffer
- Konvertering till format som Python kan hantera

### **Fas 2: Core funktionalitet (4h)**

#### **Timme 4-5: Excel-processing**
- Kopiera `flexible_excel_reader.py` till web-version
- Anpassa för Pyodide-miljö
- Implementera Excel-läsning från JavaScript

#### **Timme 6-7: PDF-generering**  
- Kopiera `pdf_generator.py` och `rapport_mall.py`
- Anpassa ReportLab för web-miljö
- Implementera PDF-download i browser

### **Fas 3: UX och polish (2h)**

#### **Timme 8: User interface**
- CSS för responsiv design
- Progress indicators under processing
- Error handling och användarfeedback

#### **Timme 9: PWA och optimering**
- Service Worker för offline-funktionalitet
- Web App Manifest för installation
- Performance-optimering och lazy loading

---

## 💻 **Kod-exempel**

### **Grundläggande HTML-struktur**
```html
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎓 LIA Rapportgenerator Web</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="manifest" href="manifest.json">
</head>
<body>
    <div class="container">
        <header>
            <h1>🎓 LIA Rapportgenerator</h1>
            <p>Automatisk generering av PDF-rapporter från Excel-filer</p>
        </header>

        <main id="app">
            <!-- Praktikinfo -->
            <section class="card">
                <h2>🏢 Praktikinfo</h2>
                <input type="text" id="practice-name" placeholder="Praktiknamn">
                <input type="text" id="practice-period" placeholder="Period">
            </section>

            <!-- Excel upload -->
            <section class="card">
                <h2>📊 Excel-fil</h2>
                <input type="file" id="excel-file" accept=".xlsx">
                <button onclick="validateFile()">Validera fil</button>
            </section>

            <!-- Generation -->
            <section class="card">
                <h2>📄 Generera rapporter</h2>
                <button onclick="generateReports()" disabled>Generera PDF-rapporter</button>
                <div class="progress-container">
                    <div class="progress-bar" id="progress"></div>
                </div>
            </section>

            <!-- Results -->
            <section class="card" id="results" style="display:none;">
                <h2>✅ Klara rapporter</h2>
                <div id="download-links"></div>
            </section>
        </main>
    </div>

    <script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
    <script src="app.js"></script>
</body>
</html>
```

### **JavaScript med Pyodide**
```javascript
// app.js
let pyodide;
let isReady = false;

// Initialisera Pyodide när sidan laddas
async function initPyodide() {
    console.log("🐍 Laddar Python runtime...");
    
    pyodide = await loadPyodide();
    
    // Installera nödvändiga Python-paket
    await pyodide.loadPackage(["pandas", "openpyxl", "micropip"]);
    
    // Installera ReportLab via micropip
    await pyodide.runPythonAsync(`
        import micropip
        await micropip.install("reportlab")
    `);
    
    // Ladda vår befintliga Python-kod
    await loadPythonModules();
    
    isReady = true;
    console.log("✅ Python redo i webbläsaren!");
}

async function loadPythonModules() {
    // Ladda flexible_excel_reader.py
    const readerResponse = await fetch('./src/flexible_excel_reader.py');
    const readerCode = await readerResponse.text();
    pyodide.runPython(readerCode);
    
    // Ladda pdf_generator.py  
    const generatorResponse = await fetch('./src/pdf_generator.py');
    const generatorCode = await generatorResponse.text();
    pyodide.runPython(generatorCode);
    
    // Ladda rapport_mall.py
    const templateResponse = await fetch('./src/rapport_mall.py');
    const templateCode = await templateResponse.text();
    pyodide.runPython(templateCode);
}

async function validateFile() {
    if (!isReady) {
        alert("⏳ Python runtime laddas fortfarande...");
        return;
    }
    
    const fileInput = document.getElementById('excel-file');
    const file = fileInput.files[0];
    
    if (!file) {
        alert("📄 Välj en Excel-fil först!");
        return;
    }
    
    try {
        // Konvertera fil till bytes för Python
        const arrayBuffer = await file.arrayBuffer();
        const bytes = new Uint8Array(arrayBuffer);
        
        // Skicka till Python för validering
        pyodide.globals.set("excel_bytes", bytes);
        pyodide.runPython(`
            import pandas as pd
            from io import BytesIO
            
            # Läs Excel-fil från bytes
            excel_buffer = BytesIO(bytes(excel_bytes))
            reader = FlexibleLIAExcelReader()
            
            try:
                df = pd.read_excel(excel_buffer)
                validation_result = reader.validate_structure(df)
                is_valid = True
            except Exception as e:
                validation_result = f"Fel: {str(e)}"
                is_valid = False
        `);
        
        // Hämta resultat från Python
        const isValid = pyodide.globals.get('is_valid');
        const result = pyodide.globals.get('validation_result');
        
        if (isValid) {
            alert("✅ Excel-filen är giltig och klar för bearbetning!");
            document.querySelector('button[onclick="generateReports()"]').disabled = false;
        } else {
            alert(`❌ Problem med Excel-filen:\n${result}`);
        }
        
    } catch (error) {
        alert(`❌ Kunde inte läsa filen: ${error.message}`);
    }
}

async function generateReports() {
    const practiceName = document.getElementById('practice-name').value;
    const practicePeriod = document.getElementById('practice-period').value;
    
    if (!practiceName || !practicePeriod) {
        alert("📝 Fyll i praktiknamn och period först!");
        return;
    }
    
    try {
        // Visa progress bar
        showProgress("🔄 Processar Excel-data...");
        
        // Kör PDF-generering i Python
        pyodide.globals.set("practice_name", practiceName);
        pyodide.globals.set("practice_period", practicePeriod);
        
        pyodide.runPython(`
            # Använd befintlig kod för att generera rapporter
            generator = PDFGenerator()
            generator.practice_name = practice_name
            generator.practice_period = practice_period
            
            # Generera alla PDFs
            pdf_files = generator.generate_all_reports_from_dataframe(df)
            
            # Konvertera till format som JavaScript kan hantera
            pdf_data = {}
            for filename, pdf_bytes in pdf_files.items():
                pdf_data[filename] = list(pdf_bytes)  # Konvertera bytes till lista
        `);
        
        updateProgress("📄 Skapar nedladdningslänkar...");
        
        // Hämta PDF-data från Python
        const pdfData = pyodide.globals.get('pdf_data').toJs();
        
        // Skapa download-länkar
        createDownloadLinks(pdfData);
        
        hideProgress();
        showResults();
        
    } catch (error) {
        hideProgress();
        alert(`❌ Fel vid generering: ${error.message}`);
    }
}

function createDownloadLinks(pdfData) {
    const container = document.getElementById('download-links');
    container.innerHTML = '';
    
    for (const [filename, bytesArray] of Object.entries(pdfData)) {
        // Konvertera tillbaka till Uint8Array
        const bytes = new Uint8Array(bytesArray);
        
        // Skapa blob och URL
        const blob = new Blob([bytes], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);
        
        // Skapa download-länk
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.textContent = `📄 ${filename}`;
        link.className = 'download-link';
        
        container.appendChild(link);
    }
}

function showProgress(message) {
    // Implementation för progress bar
}

function updateProgress(message) {
    // Update progress message
}

function hideProgress() {
    // Dölj progress bar
}

function showResults() {
    document.getElementById('results').style.display = 'block';
}

// Starta initialisering när sidan laddas
document.addEventListener('DOMContentLoaded', initPyodide);
```

### **PWA Manifest**
```json
{
    "name": "LIA Rapportgenerator",
    "short_name": "LIA Reports",
    "description": "Automatisk generering av PDF-rapporter från Excel-filer",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#2196f3",
    "orientation": "portrait-primary",
    "icons": [
        {
            "src": "icons/icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "icons/icon-512.png", 
            "sizes": "512x512",
            "type": "image/png"
        }
    ],
    "categories": ["education", "productivity", "business"]
}
```

---

## 🚀 **Distribution och access**

### **GitHub Pages deployment**
```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ web-version ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
```

### **Användar-access**
- **URL**: `https://peman68.github.io/lia-rapport-generator-web/`
- **Distribution**: Dela länk via email, Teams, intranät
- **Installation**: PWA kan installeras som app på telefon/dator
- **Uppdateringar**: Automatiska via Git push

---

## 📋 **Tekniska krav och begränsningar**

### **Browser-kompatibilitet**
- ✅ **Chrome/Edge**: Full support
- ✅ **Firefox**: Full support  
- ✅ **Safari**: Full support (iOS 14.5+)
- ⚠️ **Internet Explorer**: Inte kompatibel

### **Performance**
- **Initial load**: ~15MB (Pyodide runtime + Python paket)
- **Subsequent loads**: Cached, snabb
- **Memory usage**: ~100MB under körning
- **Processing**: Jämförbar med desktop-version

### **Säkerhet**
- ✅ **Sandbox**: All kod körs isolerat i browser
- ✅ **HTTPS**: Automatiskt med GitHub Pages
- ✅ **No server**: Ingen backend att hacka
- ✅ **Local processing**: Data lämnar aldrig användarens dator

---

## 🔄 **Framtida förbättringar**

### **Version 2.0 (ytterligare 6h)**
- **Batch processing**: Flera Excel-filer samtidigt
- **Template editor**: Anpassa PDF-layout
- **Data validation**: Mer detaljerad Excel-kontroll
- **Export options**: Olika PDF-format

### **Version 3.0 (ytterligare 9h)**  
- **Multi-language**: Engelska, andra språk
- **Cloud storage**: Integration med Google Drive/OneDrive
- **Collaboration**: Dela rapporter med kollegor
- **Analytics**: Användningsstatistik

---

## 💰 **Kostnadsanalys**

### **Utvecklingskostnad**
- **9 timmar × din timpris** = Total utvecklingskostnad
- **Jämfört med**: Extern utvecklare 15-25k SEK

### **Driftskostnad**  
- **GitHub Pages**: 0 SEK/månad
- **Netlify/Vercel**: 0 SEK/månad (gratis tier)
- **Egen domän**: 100-200 SEK/år (valfritt)

### **ROI-kalkyl**
- **Desktop-version**: Endast Windows-användare
- **Web-version**: Alla plattformar → Större användargrupp
- **Mindre support**: Ingen installation/uppdatering
- **Skalbarhet**: Obegränsat antal användare gratis

---

## 📅 **När implementera?**

### **Bra tidpunkter:**
- ✅ **Efter v1.0.0 release** (nu) - Desktop-versionen är stabil
- ✅ **Sommarsemester-projekt** - Kul sidoprojekt
- ✅ **Vid användarfeedback** - Om plattformsoberoende efterfrågas
- ✅ **Före nästa LIA-period** - Mer tid för testning

### **Prioritering:**
- 🥇 **Om Mac/Linux-användare** - Hög prioritet
- 🥈 **Om mobilanvändning** - Medel prioritet  
- 🥉 **Om bara Windows** - Låg prioritet (nuvarande räcker)

---

## 🎯 **Nästa steg när vi implementerar**

1. **Skapa feature branch**: `git checkout -b web-version`
2. **Setup GitHub Pages** på den branchen
3. **Bygg minimal prototype** (3h)
4. **Testa med riktig Excel-fil**
5. **Iterera och förbättra** (6h)
6. **Beta-test med lärare**
7. **Production release** med dokumentation

---

**Sparat för framtida implementering! 🚀**  
*Total tid: 9 timmar | Kostnad: 0 SEK hosting | Plattformar: Alla*