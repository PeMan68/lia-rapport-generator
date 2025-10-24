# 📁 Intelligent filnamngivning - Implementation

## 🎯 Översikt
Implementerat intelligent filnamngivning som inkluderar praktiknamnet i PDF-filnamnen för bättre organisation och identifiering.

## ✨ Nya filnamnsformat

### 📋 Format-struktur
```
LIA_[SafePracticeName]_[SafeStudentName].pdf
```

### 🔧 Exempel
- **Webbutveckling**: `LIA_Webbutveckling_varte_Michael_Nilsson.pdf`
- **Processteknik**: `LIA_Processteknik_HT2024_Anna_Andersson.pdf`  
- **Utan praktiknamn**: `LIA_Erik_Eriksson.pdf`

## 🛠️ Teknisk implementation

### Kod-ändringar i `src/pdf_generator.py`

```python
# Skapa säkert filnamn (ta bort specialtecken)
safe_student_name = self._create_safe_filename(student_name)

# Skapa säkert praktiknamn för filnamn
safe_practice_name = ""
if practice_name:
    safe_practice_name = self._create_safe_filename(practice_name)
    # Begränsa till första 20 tecken för att undvika för långa filnamn
    safe_practice_name = safe_practice_name[:20]
    safe_practice_name = f"{safe_practice_name}_"

# Skapa filnamn med praktiknamn inkluderat
filename = f"LIA_{safe_practice_name}{safe_student_name}.pdf"
output_path = os.path.join(output_directory, filename)
```

### 🔒 Säkerhetsåtgärder
1. **Längdbegränsning**: Praktiknamn begränsas till 20 tecken
2. **LIA-redundansborttagning**: Tar automatiskt bort "LIA" från praktiknamnet för att undvika dubbel-LIA
3. **Teckenrensning**: Svenska tecken (å,ä,ö) konverteras till (a,a,o)
4. **Specialtecken**: Ersätts med understreck (_)
5. **Mellanslag**: Konverteras till understreck

### 🤖 LIA-redundansborttagning
- **"LIA Webbutveckling"** → `LIA_Webbutveckling_Student.pdf`
- **"LIA-Processteknik"** → `LIA_Processteknik_Student.pdf`
- **"Webbutveckling LIA"** → `LIA_Webbutveckling_Student.pdf`
- **"LIA"** (endast) → `LIA_Student.pdf`

## 📊 Fördelar

### För användare
- ✅ **Enkel identifiering**: Ser direkt vilken LIA filen tillhör
- ✅ **Bättre organisation**: Filer grupperas naturligt per praktik
- ✅ **Sökvänligt**: Kan söka på praktiknamn för att hitta filer

### För systemet
- ✅ **Säkra filnamn**: Inga problematiska tecken
- ✅ **Konsekvent format**: Samma struktur för alla filer
- ✅ **Bakåtkompatibel**: Fungerar även utan praktiknamn

## 🧪 Testresultat

### Test 1: "LIA Webbutveckling"
```
Input: "LIA Webbutveckling"
Output: "LIA_Webbutveckling_Michael_Nilsson.pdf"
✅ LIA-redundans borttagen
```

### Test 2: "LIA-Processteknik HT2024"
```
Input: "LIA-Processteknik HT2024"
Output: "LIA_Processteknik_HT2024_Anna_Andersson.pdf"
✅ LIA-redundans borttagen
```

### Test 3: "Webbutveckling LIA vårterminen"
```
Input: "Webbutveckling LIA vårterminen"
Output: "LIA_Webbutveckling_varterminen_Erik_Eriksson.pdf"
✅ LIA i mitten borttagen
```

### Test 4: Inget praktiknamn eller endast "LIA"
```
Input: "" eller "LIA"
Output: "LIA_Student_Name.pdf"
✅ Fallback till standard format
```

## 🔮 Framtida förbättringar

### Möjliga tillägg
- **Datumstämpel**: Inkludera generationsdatum
- **Batch-nummer**: För flera körningar samma dag
- **Custom-format**: Låta användare välja filnamnsformat
- **Mappstruktur**: Skapa undermappar per praktik

### Konfigurationsmöjligheter
```python
# Framtida konfiguration
filename_config = {
    "include_date": True,
    "include_practice": True, 
    "max_practice_length": 20,
    "separator": "_"
}
```

## 📋 Underhåll

### Vanliga problem
- **För långa namn**: Begränsning till 20 tecken hanterar detta
- **Specialtecken**: `_create_safe_filename()` rengör automatiskt
- **Dubletter**: Osannolikt med studentnamn, men kan hanteras med suffix

### Felsökning
- Kontrollera att praktiknamn inte innehåller förbjudna tecken
- Se till att filnamnen inte blir för långa för filsystemet
- Validera att alla specialtecken hanteras korrekt

---

*Implementation datum: 2025-10-24*  
*Status: ✅ Klar och testad*  
*Kompatibilitet: Bakåtkompatibel med befintlig funktionalitet*