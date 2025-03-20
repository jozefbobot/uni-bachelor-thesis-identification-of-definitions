import tkinter as tk
import regex_identification
import os

class DefinitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Identifikácia definícií v textoch")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.active_widgets = []
        self.create_main_screen()

    def clear_screen(self):
        for widget in self.active_widgets:
            if widget.winfo_exists():
                widget.destroy()
        self.active_widgets = []

    #hlavna stranka
    def create_main_screen(self):
        #premazanie obsahu
        self.clear_screen()
        
        #názov
        title_label = tk.Label(
            self.root,
            text="Identifikácia definícií v textoch",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(35, 30))
        self.active_widgets.append(title_label)
        
        #tlačidlo pre RegEx identifikáciu
        self.regex_button = tk.Button(
            self.root,
            text="RegEx",
            command=self.show_regex_based,
            font=("Arial", 25),
            width=15,
            height=3
        )
        self.regex_button.pack(pady=(50, 20))
        self.active_widgets.append(self.regex_button)
        
        #tlačidlo pre Stanza identifikáciu
        self.stanza_button = tk.Button(
            self.root,
            text="Stanza",
            command=self.show_stanza_based,
            font=("Arial", 25),
            width=15,
            height=3
        )
        self.stanza_button.pack(pady=(10, 10))
        self.active_widgets.append(self.stanza_button)
        
        #tlačidlo pre Porovnanie
        self.comparison_button = tk.Button(
            self.root,
            text="Porovnanie",
            command=self.show_comparison,
            font=("Arial", 25),
            width=15,
            height=3
        )
        self.comparison_button.pack(pady=(10, 10))
        self.active_widgets.append(self.comparison_button)
    
    def run_regex_identification(self):
        text = self.text_field.get("1.0", "end-1c")
        
        #volanie funkcie z regex_identification.py
        definitions = regex_identification.extract_definitions(text)
        
        #vytvorenie okna pre výsledok
        result_window = tk.Toplevel(self.root)
        result_window.title("Výsledky RegEx identifikácie")
        result_window.geometry("600x400")
        
        if definitions:
            result_frame = tk.Frame(result_window)
            result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            scrollbar = tk.Scrollbar(result_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            result_text = tk.Text(result_frame, width=50, height=15, font=("Arial", 12), wrap=tk.WORD)
            result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar.config(command=result_text.yview)
            result_text.config(yscrollcommand=scrollbar.set)
            
            for term, definition in definitions:
                result_text.insert(tk.END, f"Termín: {term}\n")
                result_text.insert(tk.END, f"Definícia: {definition}\n")
                result_text.insert(tk.END, "------\n\n")
            
            result_text.config(state='disabled')  # Nastavení jen pro čtení
        else:
            no_result_label = tk.Label(
                result_window, 
                text="V texte nebola nájdená žiadna definícia",
                font=("Arial", 14)
            )
            no_result_label.pack(pady=50)
    
    def run_stanza_identification(self):
        text = self.text_field.get("1.0", "end-1c")
        
    def run_comparison(self):
        result_window = tk.Toplevel(self.root)
        result_window.title("Výsledky porovnania")
        result_window.geometry("700x500")
        
        result_frame = tk.Frame(result_window)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        result_text = tk.Text(result_frame, width=60, height=25, font=("Arial", 12), wrap=tk.WORD)
        result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=result_text.yview)
        result_text.config(yscrollcommand=scrollbar.set)
        
        result_text.insert(tk.END, "VÝSLEDKY POROVNANIA\n", "title")
        result_text.insert(tk.END, "==================\n\n", "title")
        result_text.tag_configure("title", font=("Arial", 14, "bold"))
        
        results_dir = os.path.join("results", "regex")
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        result_text.insert(tk.END, "MEDICÍNSKE TEXTY\n", "subtitle")
        result_text.tag_configure("subtitle", font=("Arial", 12, "bold"))
        
        #analýza medicínských textov
        try:
            medical_texts_path = os.path.join("texts", "medicalTexts.txt")
            with open(medical_texts_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            without_def_path = os.path.join(results_dir, "regexMedicalTextsWithoutDefinitions.txt")
            with open(without_def_path, 'w', encoding='utf-8') as without_def_file:
                
                total_texts = len(lines)
                texts_with_definitions = 0
                texts_without_definitions = 0
                total_definitions = 0
                
                for line in lines:
                    line = line.strip()
                    if line:
                        definitions = regex_identification.extract_definitions(line)
                        if definitions:
                            texts_with_definitions += 1
                            total_definitions += len(definitions)
                        else:
                            without_def_file.write(line + "\n")
                            texts_without_definitions += 1
            
            #vypočet percent
            percentage = (texts_with_definitions / total_texts * 100) if total_texts > 0 else 0
            
            #vypis vysledkov
            result_text.insert(tk.END, f"Celkový počet textov: {total_texts}\n")
            result_text.insert(tk.END, f"Počet textov s definíciami: {texts_with_definitions}\n")
            result_text.insert(tk.END, f"Počet textov bez definícií: {texts_without_definitions}\n")
            result_text.insert(tk.END, f"Percento úspešnosti: {percentage:.2f}%\n\n")
            
        except Exception as e:
            result_text.insert(tk.END, f"Chyba pri načítaní medicínskych textov: {str(e)}\n\n")
        
        #analýza zmiešaných textov
        result_text.insert(tk.END, "ZMIEŠANÉ TEXTY\n", "subtitle")
        
        try:
            mixed_texts_path = os.path.join("texts", "mixedTexts.txt")
            with open(mixed_texts_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            without_def_path = os.path.join(results_dir, "regexMixedTextsWithoutDefinitions.txt")
            with open(without_def_path, 'w', encoding='utf-8') as without_def_file:
                
                total_texts = len(lines)
                texts_with_definitions = 0
                texts_without_definitions = 0
                total_definitions = 0
                
                for line in lines:
                    line = line.strip()
                    if line:
                        definitions = regex_identification.extract_definitions(line)
                        if definitions:
                            texts_with_definitions += 1
                            total_definitions += len(definitions)
                        else:
                            without_def_file.write(line + "\n")
                            texts_without_definitions += 1
            
            #vypočet percent
            percentage = (texts_with_definitions / total_texts * 100) if total_texts > 0 else 0
            
            #vypis vysledkov
            result_text.insert(tk.END, f"Celkový počet textov: {total_texts}\n")
            result_text.insert(tk.END, f"Počet textov s definíciami: {texts_with_definitions}\n")
            result_text.insert(tk.END, f"Počet textov bez definícií: {texts_without_definitions}\n")
            result_text.insert(tk.END, f"Percento úspešnosti: {percentage:.2f}%\n\n")
            
        except Exception as e:
            result_text.insert(tk.END, f"Chyba pri načítaní zmiešaných textov: {str(e)}\n\n")
        
        #nastavenie len pre čítanie
        result_text.config(state='disabled')
        
    #regex
    def show_regex_based(self):
        #premazanie obsahu
        self.clear_screen()
        
        #tlačidlo späť
        back_button = tk.Button(
            self.root,
            text="← Späť",
            command=self.create_main_screen,
            font=("Arial", 15)
        )
        back_button.place(x=20, y=20)
        self.active_widgets.append(back_button)
        
        #nazov
        label = tk.Label(self.root, text="RegEx identifikácia", font=("Arial", 24, "bold"))
        label.pack(pady=20)
        self.active_widgets.append(label)
        
        #textove pole
        self.text_field = tk.Text(self.root, width=55, height=15, font=("Arial", 20))
        self.text_field.pack(pady=10)
        self.active_widgets.append(self.text_field)
        
        #tlačidlo pre spustenie identifikacie
        identify_button = tk.Button(
            self.root,
            text="Identifikovať",
            command=self.run_regex_identification,
            font=("Arial", 24),
            width=15,
            height=1
        )
        identify_button.pack(pady=20)
        self.active_widgets.append(identify_button)
    
    #stanza
    def show_stanza_based(self):
        #premazanie obsahu
        self.clear_screen()
        
        #tlačidlo späť
        back_button = tk.Button(
            self.root,
            text="← Späť",
            command=self.create_main_screen,
            font=("Arial", 15)
        )
        back_button.place(x=20, y=20)
        self.active_widgets.append(back_button)
        
        #nazov
        label = tk.Label(self.root, text="Stanza identifikácia", font=("Arial", 24, "bold"))
        label.pack(pady=20)
        self.active_widgets.append(label)
        
        #textove pole
        self.text_field = tk.Text(self.root, width=55, height=15, font=("Arial", 20))
        self.text_field.pack(pady=10)
        self.active_widgets.append(self.text_field)
        
        #tlačidlo pre spustenie identifikacie
        identify_button = tk.Button(
            self.root,
            text="Identifikovať",
            command=self.run_stanza_identification,
            font=("Arial", 24),
            width=15,
            height=1
        )
        identify_button.pack(pady=20)
        self.active_widgets.append(identify_button)
    
    #porovnanie
    def show_comparison(self):
        #premazanie obsahu
        self.clear_screen()
        
        #tlačidlo späť
        back_button = tk.Button(
            self.root,
            text="← Späť",
            command=self.create_main_screen,
            font=("Arial", 15)
        )
        back_button.place(x=20, y=20)
        self.active_widgets.append(back_button)
        
        #nazov
        label = tk.Label(self.root, text="Porovnanie identifikačných metód", font=("Arial", 24, "bold"))
        label.pack(pady=20)
        self.active_widgets.append(label)
        
        info_label = tk.Label(
            self.root,
            text="Kliknutím na tlačidlo sa spustí porovnanie identifikácie definícií\nv medicínskych a zmiešaných textoch",
            font=("Arial", 14),
            justify=tk.CENTER
        )
        info_label.pack(pady=50)
        self.active_widgets.append(info_label)
        
        #tlačidlo pre spustenie porovnania
        identify_button = tk.Button(
            self.root,
            text="Porovnaj",
            command=self.run_comparison,
            font=("Arial", 24),
            width=15,
            height=2
        )
        identify_button.pack(pady=20)
        self.active_widgets.append(identify_button)

if __name__ == "__main__":
    root = tk.Tk()
    app = DefinitionApp(root)
    root.mainloop()