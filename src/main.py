import tkinter as tk
from tkinter import ttk
import regex_identification
import post_identification
import os
import time

# Grafické rozhranie aplikácie
class DefinitionIdentificationApp:
    # Konštruktor
    def __init__(self, root):
        self.root = root
        self.root.title("Identifikácia definícií v textoch")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)  # Nastavenie minimálnej veľkosti okna
        
        # Získanie DPI škály pre lepšie zobrazenie na rôznych zariadeniach
        self.scale = self.get_dpi_scale()
        
        # Definovanie štýlov pre ttk
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", int(12 * self.scale)))
        self.style.configure("Large.TButton", font=("Arial", int(14 * self.scale)))
        self.style.configure("Title.TLabel", font=("Arial", int(20 * self.scale), "bold"))
        self.style.configure("Normal.TLabel", font=("Arial", int(12 * self.scale)))
        self.style.configure("MainMenu.TButton", font=("Arial", int(18 * self.scale), "bold"))
        self.style.configure("Identify.TButton", font=("Arial", int(18 * self.scale), "bold"))
        self.style.configure("Compare.TButton", font=("Arial", int(16 * self.scale), "bold"))
        
        self.active_widgets = []
        self.create_main_screen()
        
        # Nastavenie udalosti pri zmene veľkosti okna
        self.root.bind("<Configure>", self.on_resize)
    
    # Funkcia na zistenie DPI škály
    def get_dpi_scale(self):
        try:
            dpi = self.root.winfo_fpixels('1i')
            scale = dpi / 96.0  # štandardné DPI je 96
            return max(1.0, scale)
        except:
            return 1.0
    
    # Funkcia volaná pri zmene veľkosti okna
    def on_resize(self, event):
        if event.widget == self.root:
            # Možno pridať ďalšie úpravy podľa veľkosti okna
            pass

    # Funkcia na premazanie obsahu
    def clear_screen(self):
        for widget in self.active_widgets:
            if widget.winfo_exists():
                widget.destroy()
        self.active_widgets = []

    # GUI pre hlavnú stránku
    def create_main_screen(self):
        # Premazanie obsahu
        self.clear_screen()
        
        # Hlavný rámec
        main_frame = ttk.Frame(self.root, padding=(20, 20, 20, 20))
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.active_widgets.append(main_frame)
        
        # Názov hlavnej stránky s väčším písmom
        title_label = ttk.Label(
            main_frame,
            text="Identifikácia definícií v textoch",
            font=("Arial", int(28 * self.scale), "bold")  # Zväčšené písmo
        )
        title_label.pack(pady=(20 * self.scale, 50 * self.scale))
        
        # Kontajner pre tlačidlá - centrovaný
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(expand=True)
        
        # Tlačidlo pre RegEx identifikáciu
        self.regex_button = ttk.Button(
            button_frame,
            text="RegEx",
            command=self.show_regex_based,
            style="MainMenu.TButton"
        )
        # Nastavenie menšej šírky tlačidla a väčšieho vnútorného odsadenia
        self.regex_button.pack(pady=(10 * self.scale, 15 * self.scale), 
                              ipady=15 * self.scale,
                              ipadx=30 * self.scale,
                              padx=80 * self.scale)
        
        # Tlačidlo pre POST identifikáciu
        self.post_button = ttk.Button(
            button_frame,
            text="POST",
            command=self.show_post_based,
            style="MainMenu.TButton"
        )
        # Nastavenie menšej šírky tlačidla a väčšieho vnútorného odsadenia
        self.post_button.pack(pady=(0, 15 * self.scale), 
                             ipady=15 * self.scale,
                             ipadx=30 * self.scale,
                             padx=80 * self.scale)
        
        # Tlačidlo pre porovnanie metód
        self.comparison_button = ttk.Button(
            button_frame,
            text="Porovnanie",
            command=self.show_comparison,
            style="MainMenu.TButton"
        )
        # Nastavenie menšej šírky tlačidla a väčšieho vnútorného odsadenia
        self.comparison_button.pack(pady=(0, 15 * self.scale), 
                                   ipady=15 * self.scale,
                                   ipadx=30 * self.scale,
                                   padx=80 * self.scale)

    # Pomocná metóda pre vytvorenie výsledkového okna
    def create_result_window(self, title, definitions):
        # Vytvorenie okna pre výsledok
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("600x400")
        result_window.minsize(400, 300)
        
        # Ak boli nájdené definície 
        if definitions:
            # Vytvorenie scrollovateľného textového poľa pre zobrazenie výsledkov
            result_frame = ttk.Frame(result_window, padding=(10, 10, 10, 10))
            result_frame.pack(fill=tk.BOTH, expand=True)
            
            scrollbar = ttk.Scrollbar(result_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            result_text = tk.Text(
                result_frame, 
                font=("Arial", int(12 * self.scale)), 
                wrap=tk.WORD
            )
            result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=result_text.yview)
            result_text.config(yscrollcommand=scrollbar.set)
            
            # Výpis nájdených definícií
            for term, definition in definitions:
                result_text.insert(tk.END, f"Termín: {term}\n")
                result_text.insert(tk.END, f"Definícia: {definition}\n")
                result_text.insert(tk.END, "------\n\n")

            # Nastavenie len pre čítanie
            result_text.config(state='disabled')
        else: 
            # Ak neboli nájdené definície - výpis správy
            no_result_label = ttk.Label(
                result_window, 
                text="V texte nebola nájdená žiadna definícia",
                font=("Arial", int(14 * self.scale))
            )
            no_result_label.pack(pady=50, expand=True)
    
    def create_input_page(self, title, identify_command):
        # Premazanie obsahu
        self.clear_screen()
    
        # Hlavný rámec
        main_frame = ttk.Frame(self.root, padding=(20, 20, 20, 20))
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.active_widgets.append(main_frame)
    
        # Tlačidlo späť pre návrat na hlavnú stránku
        back_button = ttk.Button(
            main_frame,
            text="← Späť",
            command=self.create_main_screen
        )
        back_button.pack(anchor=tk.NW, pady=(0, 10 * self.scale))
    
        # Názov podstránky
        label = ttk.Label(
            main_frame, 
            text=title, 
            style="Title.TLabel"
        )
        label.pack(pady=(0, 15 * self.scale))
    
        # Rámec pre textové pole - nastavená maximálna výška
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10 * self.scale))
    
        # Nastavenie váhy pre riadky v main_frame, aby sa tlačidlo zobrazilo dole
        main_frame.grid_rowconfigure(0, weight=0)  # pre back_button
        main_frame.grid_rowconfigure(1, weight=0)  # pre label
        main_frame.grid_rowconfigure(2, weight=3)  # pre text_frame - väčšina priestoru
        main_frame.grid_rowconfigure(3, weight=1)  # pre tlačidlo - rezervovaný priestor dole
    
        # Scrollbar pre textové pole
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
        # Textové pole na vloženie textu - limitovaná výška
        self.text_field = tk.Text(
            text_frame, 
            font=("Arial", int(14 * self.scale)),
            wrap=tk.WORD,
            height=15  # Nastavenie fixnej výšky
        )
        self.text_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_field.yview)
        self.text_field.config(yscrollcommand=scrollbar.set)
    
        # Tlačidlo pre spustenie identifikácie v samostatnom rámci
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(20 * self.scale, 0))
    
        identify_button = ttk.Button(
            button_frame,
            text="Identifikovať",
            command=identify_command,
            style="Identify.TButton"
        )
        # Umiestnenie tlačidla na stred s menšou šírkou
        identify_button.pack(pady=10 * self.scale, ipady=8 * self.scale, 
                        anchor=tk.CENTER, expand=False,
                        padx=100 * self.scale)
    
    # Pomocná metóda pre analýzu textov
    def analyze_texts(self, text_file_path, regex_output_path, post_output_path, result_text):
        try:
            # Načítanie textov
            with open(text_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                lines = content.splitlines()
            
            # Počitadlá pre štatistiky
            total_texts = len(lines)
            
            # Analýza pomocou RegEx
            regex_texts_with_definition, regex_execution_time = self.analyze_with_method(
                lines, 
                regex_output_path, 
                regex_identification.extract_definitions
            )
            
            # Analýza pomocou part-of-speech tagging
            post_texts_with_definition, post_execution_time = self.analyze_with_method(
                lines, 
                post_output_path, 
                post_identification.extract_definitions_stanza
            )
            
            # Výpočet percent a počtu textov bez definícií
            regex_texts_without_definition = total_texts - regex_texts_with_definition
            post_texts_without_definition = total_texts - post_texts_with_definition
            regex_percentage = (regex_texts_with_definition / total_texts * 100) if total_texts > 0 else 0
            post_percentage = (post_texts_with_definition / total_texts * 100) if total_texts > 0 else 0
            
            # Výpis výsledkov pre RegEx metódu
            result_text.insert(tk.END, "\nRegEx metóda:\n", "method")
            result_text.insert(tk.END, f"Celkový počet textov: {total_texts}\n")
            result_text.insert(tk.END, f"Počet textov s definíciami: {regex_texts_with_definition}\n")
            result_text.insert(tk.END, f"Počet textov bez definícií: {regex_texts_without_definition}\n")
            result_text.insert(tk.END, f"Percento úspešnosti: {regex_percentage:.2f}%\n")
            result_text.insert(tk.END, f"Čas spracovania: {regex_execution_time:.4f} sekúnd\n\n")
            
            # Výpis výsledkov pre POST metódu
            result_text.insert(tk.END, "Part-of-speech tagging metóda:\n", "method")
            result_text.insert(tk.END, f"Celkový počet textov: {total_texts}\n")
            result_text.insert(tk.END, f"Počet textov s definíciami: {post_texts_with_definition}\n")
            result_text.insert(tk.END, f"Počet textov bez definícií: {post_texts_without_definition}\n")
            result_text.insert(tk.END, f"Percento úspešnosti: {post_percentage:.2f}%\n")
            result_text.insert(tk.END, f"Čas spracovania: {post_execution_time:.4f} sekúnd\n\n")
            
            return True
        except Exception as e:
            # Výpis chyby pri analýze textov
            result_text.insert(tk.END, f"Chyba pri analýze textov: {str(e)}\n\n")
            return False
    
    # Pomocná metóda pre analýzu s konkrétnou metódou
    def analyze_with_method(self, lines, output_path, identification_method):
        texts_with_definition = 0
        
        # Začiatok merania času
        start_time = time.time()
        
        # Otvorenie súboru pre zápis textov bez definícií
        with open(output_path, 'w', encoding='utf-8') as without_def_file:
            for line in lines:
                # Odstránenie medzier zo začiatku a konca riadku
                line = line.strip()
                if line:
                    # Volanie identifikačnej metódy
                    definition = identification_method(line)
                    if definition:
                        # Ak bola najdená definícia
                        texts_with_definition += 1
                    else:
                        # Ak nebola najdená definícia
                        without_def_file.write(line + "\n")
        
        # Koniec merania času
        end_time = time.time()
        execution_time = end_time - start_time
        
        return texts_with_definition, execution_time

    # Funkcia na identifikáciu pomocou RegEx
    def run_regex_identification(self):
        # Načítanie textu z textového poľa
        text = self.text_field.get("1.0", "end-1c")
        
        # Volanie funkcie z regex_identification.py
        definitions = regex_identification.extract_definitions(text)
        
        # Vytvorenie výsledkového okna
        self.create_result_window("Výsledky identifikácie pomocou RegEx", definitions)
    
    # Funkcia na identifikáciu pomocou part-of-speech tagging
    def run_stanza_identification(self):
        # Načítanie textu z textového poľa
        text = self.text_field.get("1.0", "end-1c")
    
        # Volanie funkcie z post_identification.py
        definitions = post_identification.extract_definitions_stanza(text)
    
        # Vytvorenie výsledkového okna
        self.create_result_window("Výsledky Stanza identifikácie", definitions)

    # Funkcia na spustenie porovnania identifikačných metód RegEx a part-of-speech tagging   
    def run_comparison(self):
        # Vytvorenie okna pre výsledky porovnania
        result_window = tk.Toplevel(self.root)
        result_window.title("Výsledky porovnania")
        result_window.geometry("800x600")
        result_window.minsize(600, 400)
        
        # Hlavný rámec pre výsledky
        result_frame = ttk.Frame(result_window, padding=(10, 10, 10, 10))
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar pre textové pole
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Textové pole pre výsledky
        result_text = tk.Text(
            result_frame, 
            font=("Arial", int(12 * self.scale)), 
            wrap=tk.WORD
        )
        result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=result_text.yview)
        result_text.config(yscrollcommand=scrollbar.set)
        
        # Vytvorenie štýlov textu
        result_text.tag_configure("title", font=("Arial", int(14 * self.scale), "bold"))
        result_text.tag_configure("subtitle", font=("Arial", int(12 * self.scale), "bold"))
        result_text.tag_configure("method", font=("Arial", int(11 * self.scale), "italic"))
        
        result_text.insert(tk.END, "VÝSLEDKY POROVNANIA\n", "title")

        # Adresáre pre ukladanie výsledkov
        regex_dir = os.path.join("results", "regex")
        post_dir = os.path.join("results", "post")
    
        # Medicínske texty
        result_text.insert(tk.END, "\nMEDICÍNSKE TEXTY\n", "subtitle")
    
        # Analýza medicínskych textov
        medical_texts_path = os.path.join("texts", "medicalTexts.txt")
        regex_without_def_path = os.path.join(regex_dir, "regexMedicalTextsWithoutDefinitions.txt")
        post_without_def_path = os.path.join(post_dir, "postMedicalTextsWithoutDefinitions.txt")
        
        self.analyze_texts(
            medical_texts_path,
            regex_without_def_path,
            post_without_def_path,
            result_text
        )
        
        # Zmiešané texty
        result_text.insert(tk.END, "\nZMIEŠANÉ TEXTY\n", "subtitle")

        # Analýza zmiešaných textov
        mixed_texts_path = os.path.join("texts", "mixedTexts.txt")
        regex_without_def_path = os.path.join(regex_dir, "regexMixedTextsWithoutDefinitions.txt")
        post_without_def_path = os.path.join(post_dir, "postMixedTextsWithoutDefinitions.txt")
        
        self.analyze_texts(
            mixed_texts_path,
            regex_without_def_path,
            post_without_def_path,
            result_text
        )
        
        # Nastavenie len pre čítanie
        result_text.config(state='disabled')
        
    # GUI pre podstránku s identifikáciou pomocou RegEx
    def show_regex_based(self):
        self.create_input_page("Identifikácia pomocou RegEx", self.run_regex_identification)
    
    # GUI pre podstránku s identifikáciou pomocou part-of-speech tagging
    def show_post_based(self):
        self.create_input_page("Identifikácia pomocou Part-of-speech tagging", self.run_stanza_identification)
    
    # GUI pre podstránku na porovnanie metód POST a RegEx
    def show_comparison(self):
        # Premazanie obsahu
        self.clear_screen()
        
        # Hlavný rámec
        main_frame = ttk.Frame(self.root, padding=(20, 20, 20, 20))
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.active_widgets.append(main_frame)
        
        # Tlačidlo späť pre návrat na hlavnú stránku
        back_button = ttk.Button(
            main_frame,
            text="← Späť",
            command=self.create_main_screen
        )
        back_button.pack(anchor=tk.NW, pady=(0, 10 * self.scale))
        
        # Názov podstránky
        label = ttk.Label(
            main_frame, 
            text="Porovnanie identifikačných metód", 
            style="Title.TLabel"
        )
        label.pack(pady=(0, 20 * self.scale))
        
        # Kontajner na presné umiestnenie informatívneho textu v strede
        center_frame = ttk.Frame(main_frame)
        center_frame.pack(fill=tk.BOTH, expand=True)
        
        # Informačný text v strede stránky
        info_label = ttk.Label(
            center_frame,
            text="Kliknutím na tlačidlo sa spustí porovnanie identifikácie definícií\nv medicínskych a zmiešaných textoch.\nPorovnávanie môže trvať až niekoľko desiatok sekúnd!",
            style="Normal.TLabel",
            justify=tk.CENTER,
            wraplength=500
        )
        # Umiestnenie informačného textu vertikálne aj horizontálne do stredu
        info_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Dolný rámec pre tlačidlo
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(0, 20 * self.scale))
        
        # Tlačidlo pre spustenie porovnania metód
        identify_button = ttk.Button(
            bottom_frame,
            text="Porovnaj",
            command=self.run_comparison,
            style="Compare.TButton"
        )
        identify_button.pack(pady=10 * self.scale, ipady=8 * self.scale, 
                           anchor=tk.CENTER, expand=False,
                           padx=100 * self.scale)

if __name__ == "__main__":
    root = tk.Tk()
    app = DefinitionIdentificationApp(root)
    root.mainloop()