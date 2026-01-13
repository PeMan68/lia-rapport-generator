# 📦 Distribution och Installation - LIA Rapportgenerator

## 🎯 Exe-fil för lärare (Enkel installation)

### ✅ **Färdig exe-fil**: `dist/LIA_Rapportgenerator.exe` (42.8 MB)

**För lärare som bara vill använda applikationen:**

### 📥 Installation
1. **Ladda ner** `LIA_Rapportgenerator.exe` från release/distribution
2. **Spara** filen i en lämplig mapp (t.ex. `C:\Program Files\LIA Rapportgenerator\`)
3. **Klicka** på exe-filen för att starta applikationen
4. **Färdig!** - Inga andra installationer behövs

### 🔒 Säkerhet
- **Windows Defender** kan varna första gången - detta är normalt för nya exe-filer
- **Klicka "Mer info"** → **"Kör ändå"** om varning visas
- Filen är säker och innehåller bara Python-applikationen

### 💾 Systemkrav
- **Windows 10/11** (64-bit)
- **Ingen Python** installation behövs
- **Cirka 50 MB** diskutrymme
- **Microsoft Office/Excel** för Excel-filer (som vanligt)

### 🚀 Användning
1. **Dubbelklicka** på `LIA_Rapportgenerator.exe`
2. **Följ användarguiden** i applikationen
3. **Välj Excel-fil** och generera rapporter

---

## 🛠️ Python-källkod (För IT/utvecklare)

### 📋 Systemkrav
- **Python 3.8+** (rekommenderat 3.13)
- **Windows 10/11**
- **Git** (för utveckling)

### 📥 Installation från källkod
```bash
# Klona repository
git clone https://github.com/PeMan68/lia-rapport-generator.git
cd lia-rapport-generator

# Skapa virtual environment
python -m venv .venv
.venv\Scripts\activate

# Installera beroenden
pip install -r requirements.txt

# Kör applikationen
python main.py
```

### 🔨 Bygga egen exe-fil

#### **Enkelt sätt (Rekommenderat)**
```bash
# Kör byggscriptet
build_exe.bat
```

#### **Manuellt sätt**
```bash
# Installera PyInstaller
pip install pyinstaller

# Bygg exe-fil med spec-filen (inkluderar alla src-moduler)
pyinstaller LIA_Rapportgenerator.spec

# Exe-fil skapas i dist/LIA_Rapportgenerator.exe
```

**OBS:** Använd `.spec`-filen för att säkerställa att alla moduler från `src/` och `templates/` inkluderas korrekt!

---

## 📁 Distributionsalternativ

### 🎯 **För lärare (Rekommenderat)**
- ✅ **Färdig exe-fil**: `LIA_Rapportgenerator.exe`
- ✅ **Inga installationer**: Klicka och kör
- ✅ **Ingen teknisk kunskap**: Behövs inte

### 🔧 **För IT-avdelningar**
- 📦 **MSI-paket**: Kan skapas för enterprise-distribution
- 🌐 **Nätverksinstallation**: Centraliserad distribution
- 📋 **Group Policy**: Automatisk installation

### 👨‍💻 **För utvecklare**
- 📄 **Källkod**: Fullständig Python-implementation
- 🔄 **Git repository**: Version control och samarbete
- 🧪 **Development environment**: Lokal utveckling

---

## 🗂️ Distributionspaket

### 📦 **Release v1.0.0 innehåller:**

#### **För användare:**
- `LIA_Rapportgenerator.exe` - Färdig applikation
- `README.md` - Översikt och snabbstart
- `docs/ANVÄNDARMANUAL.md` - Detaljerad användning

#### **För utvecklare:**
- Fullständig källkod i `src/`
- `requirements.txt` - Python-beroenden
- `templates/` - PDF-rapportmallar
- Komplett dokumentation i `docs/`

#### **Teknisk info:**
- `VERSION.md` - Release-anteckningar
- `PROJEKTPLAN.md` - Utvecklingshistoria
- `.gitignore` - Git-konfiguration

---

## 🔄 Uppdateringar

### **Version 1.0.0**
- ✅ Flexibel Excel-läsare
- ✅ Intelligent filnamning
- ✅ Professionell PDF-layout
- ✅ Användarvänlig GUI
- ✅ Produktionsklar exe-fil

### **Framtida versioner**
- 🔄 Automatiska uppdateringar
- 📧 E-post integration
- 🎨 Anpassningsbara mallar
- 📊 Batch-processning

---

## 🏢 Enterprise-distribution

### **För skolor/organisationer:**

#### **Option 1: Enkel distribution**
1. Ladda ner `LIA_Rapportgenerator.exe`
2. Placera på gemensam nätverksdisk
3. Skapa genväg på lärardatorer
4. Informera lärare om användning

#### **Option 2: Centraliserad installation**
1. Använd software deployment verktyg
2. Distribuera via Group Policy
3. Installera i Program Files
4. Skapa Desktop shortcuts automatiskt

#### **Support och utbildning**
- 📚 Användarmanual finns tillgänglig
- 🎥 Video-tutorials kan skapas
- 💬 Teknisk support via IT-avdelning
- 📞 Utvecklingsupport vid behov

---

*För teknisk support eller frågor om distribution, kontakta utvecklingsteamet.*