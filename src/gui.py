"""
GUI för LIA PDF-rapportgenerator
Enkelt gränssnitt för lärare att generera PDF-rapporter från Excel-filer
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path

# Lägg till src-mappen till Python path
current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, project_root)

from pdf_generator import LIAPDFGenerator

class LIAReportGUI:
    """Huvudklass för GUI-applikationen"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("LIA Rapportgenerator v1.0")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Variabler
        self.excel_file_path = tk.StringVar()
        self.output_directory = tk.StringVar()
        self.generator = LIAPDFGenerator()
        self.students_data = []
        
        # Sätt default output directory
        self.output_directory.set(os.path.join(os.getcwd(), "output"))
        
        self.setup_ui()
        
    def setup_ui(self):
        """Skapar användargränssnittet"""
        
        # Huvudstil
        style = ttk.Style()
        style.theme_use('clam')
        
        # Huvudram
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Konfigurera grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Titel
        title_label = ttk.Label(
            main_frame, 
            text="LIA RAPPORTGENERATOR", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Excel-fil sektion
        ttk.Label(main_frame, text="1. Välj Excel-fil:", font=("Arial", 12, "bold")).grid(
            row=1, column=0, columnspan=3, sticky=tk.W, pady=(0, 5)
        )
        
        ttk.Entry(
            main_frame, 
            textvariable=self.excel_file_path, 
            width=60,
            state="readonly"
        ).grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(
            main_frame, 
            text="Välj fil...", 
            command=self.select_excel_file
        ).grid(row=2, column=2, sticky=tk.W)
        
        # Output-mapp sektion
        ttk.Label(main_frame, text="2. Välj utdatamapp:", font=("Arial", 12, "bold")).grid(
            row=3, column=0, columnspan=3, sticky=tk.W, pady=(20, 5)
        )
        
        ttk.Entry(
            main_frame, 
            textvariable=self.output_directory, 
            width=60
        ).grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(
            main_frame, 
            text="Välj mapp...", 
            command=self.select_output_directory
        ).grid(row=4, column=2, sticky=tk.W)
        
        # Validering och förhandsvisning
        validation_frame = ttk.LabelFrame(main_frame, text="3. Förhandsvisning", padding="10")
        validation_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        validation_frame.columnconfigure(0, weight=1)
        
        # Info-text
        self.info_text = scrolledtext.ScrolledText(
            validation_frame, 
            height=8, 
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        validation_frame.rowconfigure(0, weight=1)
        
        # Knappar
        button_frame = ttk.Frame(validation_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(1, weight=1)
        
        self.validate_button = ttk.Button(
            button_frame, 
            text="Validera Excel-fil", 
            command=self.validate_excel_file
        )
        self.validate_button.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.generate_button = ttk.Button(
            button_frame, 
            text="Generera alla rapporter", 
            command=self.generate_all_reports,
            state="disabled"
        )
        self.generate_button.grid(row=0, column=2, sticky=tk.E)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            validation_frame, 
            mode='determinate'
        )
        self.progress.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(validation_frame, text="Välj Excel-fil för att börja")
        self.status_label.grid(row=3, column=0, pady=(5, 0))
        
        # Initial info
        self.display_info("Välkommen till LIA Rapportgenerator!\n\n"
                         "Steg:\n"
                         "1. Välj din Excel-fil med LIA-bedömningar\n"
                         "2. Välj mapp där PDF-rapporter ska sparas\n"
                         "3. Klicka 'Validera Excel-fil' för att kontrollera\n"
                         "4. Klicka 'Generera alla rapporter' för att skapa PDF:er\n\n"
                         "Tips: Excel-filen bör ha kolumner som 'Q1: Namn Yh-studerande', "
                         "'Q2: Namn företag', etc.")
    
    def select_excel_file(self):
        """Öppnar fildialogruta för att välja Excel-fil"""
        file_path = filedialog.askopenfilename(
            title="Välj Excel-fil med LIA-bedömningar",
            filetypes=[
                ("Excel-filer", "*.xlsx *.xls"),
                ("Alla filer", "*.*")
            ]
        )
        
        if file_path:
            self.excel_file_path.set(file_path)
            self.display_info(f"Excel-fil vald: {file_path}\n\n"
                             "Klicka 'Validera Excel-fil' för att kontrollera innehållet.")
            self.generate_button.config(state="disabled")
    
    def select_output_directory(self):
        """Öppnar mappdialogruta för att välja utdatamapp"""
        directory = filedialog.askdirectory(
            title="Välj mapp för PDF-rapporter",
            initialdir=self.output_directory.get()
        )
        
        if directory:
            self.output_directory.set(directory)
    
    def validate_excel_file(self):
        """Validerar vald Excel-fil"""
        excel_path = self.excel_file_path.get()
        
        if not excel_path:
            messagebox.showerror("Fel", "Välj en Excel-fil först")
            return
        
        if not os.path.exists(excel_path):
            messagebox.showerror("Fel", "Excel-filen existerar inte")
            return
        
        self.status_label.config(text="Validerar Excel-fil...")
        self.validate_button.config(state="disabled")
        
        # Kör validering i separat tråd för att inte frysa GUI
        threading.Thread(target=self._validate_excel_thread, daemon=True).start()
    
    def _validate_excel_thread(self):
        """Kör Excel-validering i bakgrundstråd"""
        try:
            excel_path = self.excel_file_path.get()
            validation_result = self.generator.validate_excel_structure(excel_path)
            
            # Uppdatera GUI från main thread
            self.root.after(0, self._handle_validation_result, validation_result)
            
        except Exception as e:
            error_msg = f"Fel vid validering: {str(e)}"
            self.root.after(0, self._handle_validation_error, error_msg)
    
    def _handle_validation_result(self, validation_result):
        """Hanterar resultat från Excel-validering"""
        self.validate_button.config(state="normal")
        
        if validation_result['valid']:
            student_count = validation_result['student_count']
            students = validation_result['students']
            
            info_text = f"✅ Excel-fil validerad framgångsrikt!\n\n"
            info_text += f"Antal studenter: {student_count}\n\n"
            info_text += "Studenter som hittades:\n"
            
            for i, student in enumerate(students, 1):
                info_text += f"{i:2d}. {student}\n"
            
            if validation_result.get('has_more', False):
                info_text += f"... och {student_count - len(students)} till\n"
            
            info_text += f"\nUtdatamapp: {self.output_directory.get()}\n"
            info_text += f"\nKlicka 'Generera alla rapporter' för att skapa {student_count} PDF-filer."
            
            self.display_info(info_text)
            self.generate_button.config(state="normal")
            self.status_label.config(text=f"Redo att generera {student_count} rapporter")
            
        else:
            error_msg = validation_result['error']
            self.display_info(f"❌ Excel-fil ogiltig\n\n"
                             f"Fel: {error_msg}\n\n"
                             f"Kontrollera att Excel-filen har rätt format med kolumner som:\n"
                             f"- Q1: Namn Yh-studerande\n"
                             f"- Q2: Namn företag\n"
                             f"- Q3: Namn handledare\n"
                             f"- Q5-Q32: Bedömningar\n"
                             f"- Q33: Helhetsintryck")
            self.status_label.config(text="Excel-fil ogiltig")
    
    def _handle_validation_error(self, error_msg):
        """Hanterar fel från Excel-validering"""
        self.validate_button.config(state="normal")
        self.display_info(f"❌ Fel vid validering\n\n{error_msg}")
        self.status_label.config(text="Fel vid validering")
    
    def generate_all_reports(self):
        """Genererar alla PDF-rapporter"""
        excel_path = self.excel_file_path.get()
        output_dir = self.output_directory.get()
        
        if not excel_path or not output_dir:
            messagebox.showerror("Fel", "Välj både Excel-fil och utdatamapp")
            return
        
        # Bekräfta innan generering
        result = messagebox.askyesno(
            "Bekräfta generering",
            f"Generera PDF-rapporter för alla studenter?\n\n"
            f"Excel-fil: {os.path.basename(excel_path)}\n"
            f"Utdatamapp: {output_dir}\n\n"
            f"Detta kan ta en stund beroende på antal studenter."
        )
        
        if not result:
            return
        
        self.generate_button.config(state="disabled")
        self.validate_button.config(state="disabled")
        self.status_label.config(text="Genererar rapporter...")
        
        # Kör generering i separat tråd
        threading.Thread(target=self._generate_reports_thread, daemon=True).start()
    
    def _generate_reports_thread(self):
        """Kör PDF-generering i bakgrundstråd"""
        try:
            excel_path = self.excel_file_path.get()
            output_dir = self.output_directory.get()
            
            # Ladda Excel-data
            self.root.after(0, self._update_progress, 0, "Laddar Excel-data...")
            
            if not self.generator.load_excel_file(excel_path):
                raise Exception("Kunde inte ladda Excel-fil")
            
            # Generera rapporter
            generated_files = self.generator.generate_all_reports(output_dir)
            
            # Uppdatera GUI med resultat
            self.root.after(0, self._handle_generation_result, generated_files, output_dir)
            
        except Exception as e:
            error_msg = f"Fel vid generering: {str(e)}"
            self.root.after(0, self._handle_generation_error, error_msg)
    
    def _update_progress(self, value, status_text):
        """Uppdaterar progress bar och status"""
        self.progress['value'] = value
        self.status_label.config(text=status_text)
    
    def _handle_generation_result(self, generated_files, output_dir):
        """Hanterar resultat från PDF-generering"""
        self.generate_button.config(state="normal")
        self.validate_button.config(state="normal")
        self.progress['value'] = 100
        
        if generated_files:
            success_count = len(generated_files)
            
            info_text = f"🎉 Generering slutförd!\n\n"
            info_text += f"Antal rapporter skapade: {success_count}\n"
            info_text += f"Sparade i: {output_dir}\n\n"
            info_text += "Skapade filer:\n"
            
            for student, filepath in generated_files.items():
                filename = os.path.basename(filepath)
                info_text += f"📄 {student}: {filename}\n"
            
            info_text += f"\n✅ Alla rapporter är redo att användas!"
            
            self.display_info(info_text)
            self.status_label.config(text=f"Klart! {success_count} rapporter skapade")
            
            # Visa bekräftelse och fråga om att öppna mappen
            result = messagebox.askyesno(
                "Generering slutförd",
                f"✅ {success_count} PDF-rapporter skapades framgångsrikt!\n\n"
                f"Vill du öppna utdatamappen i Utforskaren?"
            )
            
            if result:
                try:
                    os.startfile(output_dir)
                except:
                    pass  # Ignorera fel om vi inte kan öppna mappen
        else:
            self.display_info("❌ Inga rapporter kunde skapas\n\nKontrollera Excel-filen och försök igen.")
            self.status_label.config(text="Fel: Inga rapporter skapades")
    
    def _handle_generation_error(self, error_msg):
        """Hanterar fel från PDF-generering"""
        self.generate_button.config(state="normal")
        self.validate_button.config(state="normal")
        self.progress['value'] = 0
        self.display_info(f"❌ Fel vid generering\n\n{error_msg}")
        self.status_label.config(text="Fel vid generering")
        messagebox.showerror("Generering misslyckades", error_msg)
    
    def display_info(self, text):
        """Visar information i textområdet"""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)


def main():
    """Huvudfunktion som startar GUI-applikationen"""
    root = tk.Tk()
    app = LIAReportGUI(root)
    
    # Sätt ikoner och stil
    try:
        # Försök att sätta ikon om den finns
        root.iconbitmap('icon.ico')
    except:
        pass  # Ignorera om ikon inte finns
    
    # Starta GUI
    root.mainloop()


if __name__ == "__main__":
    main()