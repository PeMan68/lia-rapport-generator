# 📚 Användarmanual - LIA Rapportgenerator

## 🎯 Översikt
LIA Rapportgenerator är ett användarvänligt verktyg som automatiskt skapar individuella PDF-rapporter från Excel-filer med LIA-bedömningar. Applikationen **anpassar sig automatiskt** till olika Excel-format.

## 🚀 Komma igång

### 1. Starta applikationen
```bash
python main.py
```

### 2. Huvudgränssnitt
När applikationen startar ser du ett enkelt gränssnitt med följande sektioner:

#### **Praktikinfo** 🏢
- **Praktiknamn**: Ange namnet på praktiken (t.ex. "Webbutveckling vårterminen")
- **Period**: Ange praktikperioden (t.ex. "VT 2024" eller "2024-03-01 till 2024-05-31")

#### **Excel-fil** 📊
- **Välj fil**: Klicka för att välja din Excel-fil med LIA-bedömningar
- **Validera**: Kontrollerar att filen är korrekt formaterad

#### **Utdata** 📁
- **Utdatamapp**: Ange var PDF-rapporterna ska sparas
- **Generera**: Skapar alla PDF-rapporter

## 📋 Steg-för-steg guide

### Steg 1: Praktikinfo
1. Fyll i **Praktiknamn** (visas i rapportrubriken)
2. Fyll i **Period** (visas i rapporten)

### Steg 2: Välj Excel-fil
1. Klicka **"Välj fil..."**
2. Navigera till din Excel-fil
3. Välj filen (stödjer .xlsx format)
4. ✅ **Automatisk formatidentifiering** - applikationen anpassar sig till din filstruktur

### Steg 3: Validera fil
1. Klicka **"Validera Excel-fil"**
2. Vänta på valideringsresultat
3. ✅ Grön text = Allt OK
4. ❌ Röd text = Problem som behöver åtgärdas

### Steg 4: Välj utdatamapp
1. Ange sökväg där PDF:erna ska sparas
2. Mappen skapas automatiskt om den inte finns

### Steg 5: Generera rapporter
1. Klicka **"Generera alla rapporter"**
2. Se progressbar för framsteg
3. Vänta tills alla rapporter är klara
4. ✅ **Framgångsrikt!** - PDF:erna finns nu i din utdatamapp

## 📊 Excel-filformat som stöds

### 🔧 Automatisk anpassning
Applikationen stödjer olika Excel-format automatiskt:

#### **Grundläggande struktur**
- **Q1-Q4**: Grundinfo (student, företag, handledare, närvarotid)
- **Q5-QX**: Bedömningsområden med kommentarer
- **Sista Q:n**: Helhetsintryck/slutbetyg
- **Sista+1**: Slutkommentarer

#### **Exempel på stödda format**
- **Webbutveckling**: Q1-Q34 (14 bedömningsområden)
- **Processteknik**: Q1-Q30 (12 bedömningsområden)
- **Andra program**: Liknande struktur med varierande antal Q-frågor

### ⚡ Automatisk identifiering
Applikationen hittar automatiskt:
- ✅ Studentnamn (oavsett exakt kolumnnamn)
- ✅ Företag och handledare
- ✅ Bedömningsområden och kommentarer
- ✅ Slutbetyg och slutkommentarer

## 📄 Genererade PDF-rapporter

### 📝 Innehåll
Varje PDF-rapport innehåller:

#### **Rubrik**
- Praktiknamn och period (från dina inställningar)
- Professional utseende

#### **Grundinformation**
- Studentens namn
- Företag och handledare
- Närvarotid
- Praktiknamn och period

#### **Bedömningar**
- Alla bedömningsområden med betyg
- Kommentarer för varje område
- Tydlig struktur och läsbarhet

#### **Sammanfattning**
- Helhetsintryck/slutbetyg
- Betygsfördelning (statistik)
- Slutkommentarer

### 🎨 Layout
- **Professionell design** med tydliga sektioner
- **Svart text** för optimal läsbarhet
- **Korrekt svenska tecken** (ö, ä, å)
- **Strukturerade tabeller** för bedömningar
- **Intelligent filnamn**: `LIA_[Praktiknamn]_[Studentnamn].pdf`

### 📁 Filnamnsexempel
- **Med praktiknamn**: `LIA_Webbutveckling_Michael_Nilsson.pdf` (från "LIA Webbutveckling")
- **Kort praktiknamn**: `LIA_Processteknik_HT2024_Anna_Andersson.pdf`
- **Utan praktiknamn**: `LIA_Erik_Eriksson.pdf`
- **Smart LIA-borttagning**: Automatiskt undviker dubbel-LIA i filnamn

## ❗ Felsökning

### Vanliga problem

#### **"Kunde inte läsa Excel-fil"**
- ✅ Kontrollera att filen är .xlsx format
- ✅ Se till att filen inte är öppen i Excel
- ✅ Kontrollera filsökvägen

#### **"Excel-filen har inte rätt struktur"**
- ✅ Kontrollera att filen har Q1-Q4 grundkolumner
- ✅ Se till att det finns bedömningsområden (Q5+)
- ✅ Kontrollera att det finns slutbetyg och kommentarer

#### **"Ingen studentdata hittades"**
- ✅ Kontrollera att det finns rader med data
- ✅ Se till att studentnamn är ifyllt
- ✅ Kontrollera att betygsinformation finns

### Loggar och debug
- Applikationen visar detaljerade meddelanden i konsolen
- Grön text = framgång, röd text = problem
- Spara felmeddelanden för support

## 💡 Tips för bästa resultat

### Excel-förberedelser
1. **Stäng Excel-filen** innan du kör applikationen
2. **Kontrollera data** - se till att alla obligatoriska fält är ifyllda
3. **Backup** - gör en kopia av Excel-filen först

### Praktikinfo
1. **Beskrivande namn** - hjälper att identifiera rapporter senare
2. **Tydlig period** - gör rapporterna mer professionella
3. **Konsekvent formatering** - använd samma format för alla körningar

### Utdata
1. **Egen mapp** - skapa en särskild mapp för varje praktikperiod
2. **Säkra namn** - undvik specialtecken i mappsökvägar
3. **Backup** - spara genererade PDF:er på säker plats

## 🔮 Framtida funktioner

Planerade förbättringar:
- **Batch-processning**: Hantera flera Excel-filer samtidigt
- **Template-anpassning**: Möjlighet att anpassa PDF-layout
- **Export-alternativ**: Andra format än PDF
- **Automatisk e-post**: Skicka rapporter direkt till studenter

---

*För teknisk support eller frågor, kontakta utvecklingsteamet eller se den tekniska dokumentationen.*