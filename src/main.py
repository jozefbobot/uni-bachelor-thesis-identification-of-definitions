import tkinter as tk
import regex_identification
import post_identification
import os
import time

#grafivké rozhranie aplikácie
class DefinitionIdentificationApp:
    #konštruktor
    def __init__(self, root):
        self.root = root
        self.root.title("Identifikácia definícií v textoch")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.active_widgets = []
        self.create_main_screen()

    #funkcia na premazanie obsahu
    def clear_screen(self):
        for widget in self.active_widgets:
            if widget.winfo_exists():
                widget.destroy()
        self.active_widgets = []

    #GUI pre hlavnu stránka
    def create_main_screen(self):
        #premazanie obsahu
        self.clear_screen()
        
        #názov hlavnej stránky
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
        
        #tlačidlo pre POST identifikáciu
        self.post_button = tk.Button(
            self.root,
            text="POST",
            command=self.show_post_based,
            font=("Arial", 25),
            width=15,
            height=3
        )
        self.post_button.pack(pady=(10, 10))
        self.active_widgets.append(self.post_button)
        
        #tlačidlo pre porovnanie metód RegEx a Part-of-speech tagging
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
    
    #funkcia na identifikáciu pomocou RegEx
    def run_regex_identification(self):
        #načítanie textu z textového poľa
        text = self.text_field.get("1.0", "end-1c")
        
        #volanie funkcie z regex_identification.py
        definitions = regex_identification.extract_definitions(text)
        
        #vytvorenie okna pre výsledok
        result_window = tk.Toplevel(self.root)
        result_window.title("Výsledky identifikácie pomocou RegEx")
        result_window.geometry("600x400")
        
        #ak boli nájdené definície 
        if definitions:
            #vytvorenie scrollovateľného textového poľa pre zobrazenie výsledkov
            result_frame = tk.Frame(result_window)
            result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            scrollbar = tk.Scrollbar(result_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            result_text = tk.Text(result_frame, width=50, height=15, font=("Arial", 12), wrap=tk.WORD)
            result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=result_text.yview)
            result_text.config(yscrollcommand=scrollbar.set)
            
            #výpis nájdených definícií
            for term, definition in definitions:
                result_text.insert(tk.END, f"Termín: {term}\n")
                result_text.insert(tk.END, f"Definícia: {definition}\n")
                result_text.insert(tk.END, "------\n\n")

            #nastavenie len pre čítanie
            result_text.config(state='disabled')
        else: 
            #ak neboli nájdené definície - výpis správy pri nenajdení žiadnej defincie
            no_result_label = tk.Label(
                result_window, 
                text="V texte nebola nájdená žiadna definícia",
                font=("Arial", 14)
            )
            no_result_label.pack(pady=50)
    
    #funkcia na identifikáciu pomocou part-of-speech tagging
    def run_stanza_identification(self):
        #načítanie textu z textového poľa
        text = self.text_field.get("1.0", "end-1c")
    
        #volanie funkcie z post_identification.py
        definitions = post_identification.extract_definitions_stanza(text)
    
        #vytvorenie okna pre výsledok
        result_window = tk.Toplevel(self.root)
        result_window.title("Výsledky Stanza identifikácie")
        result_window.geometry("600x400")

        #ak boli nájdené definície
        if definitions:
            #vytvorenie scrollovateľného textového poľa pre zobrazenie výsledkov
            result_frame = tk.Frame(result_window)
            result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            scrollbar = tk.Scrollbar(result_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            result_text = tk.Text(result_frame, width=50, height=15, font=("Arial", 12), wrap=tk.WORD)
            result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=result_text.yview)
            result_text.config(yscrollcommand=scrollbar.set)

            #výpis nájdených definícií
            for term, definition in definitions:
                result_text.insert(tk.END, f"Termín: {term}\n")
                result_text.insert(tk.END, f"Definícia: {definition}\n")
                result_text.insert(tk.END, "------\n\n")

            #nastavenie len pre čítanie
            result_text.config(state='disabled')
        else: 
            #ak neboli nájdené definície - výpis správy pri nenajdení žiadnej defincie
            no_result_label = tk.Label(
                result_window, 
                text="V texte nebola nájdená žiadna definícia",
                font=("Arial", 14)
            )
            no_result_label.pack(pady=50)

    #funkcia na spustenie porovnania identifikačných metód RegEx a part-of-speech tagging   
    def run_comparison(self):
        #vytvorenie okna pre výsledky porovnania
        result_window = tk.Toplevel(self.root)
        result_window.title("Výsledky porovnania")
        result_window.geometry("800x600")
        result_frame = tk.Frame(result_window)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_text = tk.Text(result_frame, width=60, height=25, font=("Arial", 12), wrap=tk.WORD)
        result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=result_text.yview)
        result_text.config(yscrollcommand=scrollbar.set)
        result_text.insert(tk.END, "VÝSLEDKY POROVNANIA\n", "title")
        result_text.tag_configure("title", font=("Arial", 14, "bold"))

        #adresáre pre ukladanie výsledkov
        regex_dir = os.path.join("results", "regex")
        post_dir = os.path.join("results", "post")
    
        #medicínske texty
        result_text.insert(tk.END, "MEDICÍNSKE TEXTY\n", "subtitle")
        result_text.tag_configure("subtitle", font=("Arial", 12, "bold"))
    
        #analýza medicínskych textov
        try:
            #načítanie medicínskych textov
            medical_texts_path = os.path.join("texts", "medicalTexts.txt")
            with open(medical_texts_path, 'r', encoding='utf-8') as file:
                med_content = file.read()
                lines = med_content.splitlines()
        
            #analýza pomocou RegEx
            #cesta k súboru pre texty bez definícií
            regex_without_def_path = os.path.join(regex_dir, "regexMedicalTextsWithoutDefinitions.txt")

            #otvorenie súboru pre zápis textov bez definícií
            with open(regex_without_def_path, 'w', encoding='utf-8') as without_def_file:
                #počitadlá pre štatistiky
                total_texts = len(lines)
                regex_texts_with_definition = 0
                regex_texts_without_definition = 0

                #začiatok merania času pre RegEx
                regex_start_time = time.time()
            
                for line in lines:
                    #odstránenie medzier zo začiatku a konca riadku
                    line = line.strip()
                    if line: 
                        #ak riadok nie je prázdny zavola funkcie z regex_identification.py s riadkom textu
                        definition = regex_identification.extract_definitions(line)
                        if definition:
                            #ak bola najdená definícia zvyši počet textov s definíciami
                            regex_texts_with_definition += 1
                        else:
                            #ak nebola najdena definícia zapíše sa text do súboru a zvýši sa počet textov bez definícií
                            without_def_file.write(line + "\n")
                            regex_texts_without_definition += 1

                #koniec merania času pre RegEx
                regex_end_time = time.time()
                regex_execution_time = regex_end_time - regex_start_time

            #analýza pomocou part-of-speech tagging
            #cesta k súboru pre texty bez definícií
            post_without_def_path = os.path.join(post_dir, "postMedicalTextsWithoutDefinitions.txt")

            #otvorenie súboru pre zápis textov bez definícií
            with open(post_without_def_path, 'w', encoding='utf-8') as without_def_file:
                #počitadlá pre štatistiky
                post_texts_with_definition = 0
                post_texts_without_definition = 0

                #začiatok merania času pre POST
                post_start_time = time.time()
            
                for line in lines:
                    #odstránenie medzier zo začiatku a konca riadku
                    line = line.strip()
                    if line:
                        #ak riadok nie je prázdny zavola funkcie z post_identification.py s riadkom textu
                        definition = post_identification.extract_definitions_stanza(line)
                        if definition:
                            #ak bola najdena definícia zvyši počet textov s definíciami
                            post_texts_with_definition += 1
                        else:
                            #ak nebola najdena definícia zapíše sa text do súboru a zvýši sa počet textov bez definícií
                            without_def_file.write(line + "\n")
                            post_texts_without_definition += 1

                # Koniec merania času pre POST
                post_end_time = time.time()
                post_execution_time = post_end_time - post_start_time

            #výpočet percent
            regex_percentage = (regex_texts_with_definition / total_texts * 100) if total_texts > 0 else 0
            post_percentage = (post_texts_with_definition / total_texts * 100) if total_texts > 0 else 0
        
            #výpis výsledkov pre medicínske texty
            #metoda RegEx
            result_text.insert(tk.END, "RegEx metóda:\n", "method")
            result_text.tag_configure("method", font=("Arial", 11, "italic"))
            result_text.insert(tk.END, f"Celkový počet textov: {total_texts}\n")
            result_text.insert(tk.END, f"Počet textov s definíciami: {regex_texts_with_definition}\n")
            result_text.insert(tk.END, f"Počet textov bez definícií: {regex_texts_without_definition}\n")
            result_text.insert(tk.END, f"Percento úspešnosti: {regex_percentage:.2f}%\n\n")
            result_text.insert(tk.END, f"Čas spracovania: {regex_execution_time:.4f} sekúnd\n\n")

            #metoda POST
            result_text.insert(tk.END, "Part-of-speech tagging metóda:\n", "method")
            result_text.insert(tk.END, f"Celkový počet textov: {total_texts}\n")
            result_text.insert(tk.END, f"Počet textov s definíciami: {post_texts_with_definition}\n")
            result_text.insert(tk.END, f"Počet textov bez definícií: {post_texts_without_definition}\n")
            result_text.insert(tk.END, f"Percento úspešnosti: {post_percentage:.2f}%\n\n")
            result_text.insert(tk.END, f"Čas spracovania: {post_execution_time:.4f} sekúnd\n\n")

        
        except Exception as e:
            #výpis chyby pri analýze medicínskych textov
            result_text.insert(tk.END, f"Chyba pri analýze medicínskych textov: {str(e)}\n\n")
    
        #zmiešané texty
        result_text.insert(tk.END, "ZMIEŠANÉ TEXTY\n", "subtitle")

        #analýza zmiešaných textov
        try:
            #načítanie zmiešaných textov
            mixed_texts_path = os.path.join("texts", "mixedTexts.txt")
            with open(mixed_texts_path, 'r', encoding='utf-8') as file:
                mix_content = file.read()
                lines = mix_content.splitlines()
        
            #analýza pomocou RegEx
            #cesta k súboru pre texty bez definícií
            regex_without_def_path = os.path.join(regex_dir, "regexMixedTextsWithoutDefinitions.txt")

            #otvorenie súboru pre zápis textov bez definícií
            with open(regex_without_def_path, 'w', encoding='utf-8') as without_def_file:
                #počitadlá pre štatistiky
                total_texts = len(lines)
                regex_texts_with_definition = 0
                regex_texts_without_definition = 0

                #začiatok merania času pre RegEx
                regex_start_time = time.time()
            
                for line in lines:
                    #odstránenie medzier zo začiatku a konca riadku
                    line = line.strip()
                    if line:
                        #ak riadok nie je prázdny zavola funkcie z regex_identification.py s riadkom textu
                        definition = regex_identification.extract_definitions(line)
                        if definition:
                            #ak boli nájdené definície zvyši počet textov s definíciami
                            regex_texts_with_definition += 1
                        else:
                            #ak nebola najdena definícia zapíše sa text do súboru a zvýši sa počet textov bez definícií
                            without_def_file.write(line + "\n")
                            regex_texts_without_definition += 1
                
                #koniec merania času pre RegEx
                regex_end_time = time.time()
                regex_execution_time = regex_end_time - regex_start_time
        
            #analýza pomocou part-of-speech tagging
            #cesta k súboru pre texty bez definícií
            pos_without_def_path = os.path.join(post_dir, "postMixedTextsWithoutDefinitions.txt")

            #otvorenie súboru pre zápis textov bez definícií
            with open(pos_without_def_path, 'w', encoding='utf-8') as without_def_file:
                #počitadlá pre štatistiky
                post_texts_with_definition = 0
                post_texts_without_definition = 0

                # Začiatok merania času pre POST
                post_start_time = time.time()
            
                for line in lines:
                    #odstránenie medzier zo začiatku a konca riadku
                    line = line.strip()
                    if line:
                        #ak riadok nie je prázdny zavola funkcie z post_identification.py s riadkom textu
                        definition = post_identification.extract_definitions_stanza(line)
                        if definition:
                            #ak bola najdená definícia zvyši počet textov s definíciami
                            post_texts_with_definition += 1
                        else:
                            #ak nebola najdena definícia zapíše sa text do súboru a zvýši sa počet textov bez definícií
                            without_def_file.write(line + "\n")
                            post_texts_without_definition += 1
                
                #koniec merania času pre POST
                post_end_time = time.time()
                post_execution_time = post_end_time - post_start_time

            #výpočet percent
            regex_percentage = (regex_texts_with_definition / total_texts * 100) if total_texts > 0 else 0
            post_percentage = (post_texts_with_definition / total_texts * 100) if total_texts > 0 else 0

            #výpis výsledkov pre medicínske texty
            #metoda RegEx
            result_text.insert(tk.END, "RegEx metóda:\n", "method")
            result_text.insert(tk.END, f"Celkový počet textov: {total_texts}\n")
            result_text.insert(tk.END, f"Počet textov s definíciami: {regex_texts_with_definition}\n")
            result_text.insert(tk.END, f"Počet textov bez definícií: {regex_texts_without_definition}\n")
            result_text.insert(tk.END, f"Percento úspešnosti: {regex_percentage:.2f}%\n\n")
            result_text.insert(tk.END, f"Čas spracovania: {regex_execution_time:.4f} sekúnd\n\n")

            #metoda POST
            result_text.insert(tk.END, "Part-of-speech tagging metóda:\n", "method")
            result_text.insert(tk.END, f"Celkový počet textov: {total_texts}\n")
            result_text.insert(tk.END, f"Počet textov s definíciami: {post_texts_with_definition}\n")
            result_text.insert(tk.END, f"Počet textov bez definícií: {post_texts_without_definition}\n")
            result_text.insert(tk.END, f"Percento úspešnosti: {post_percentage:.2f}%\n\n")
            result_text.insert(tk.END, f"Čas spracovania: {post_execution_time:.4f} sekúnd\n\n")
        
        except Exception as e:
            #výpis chyby pri analýze zmiešaných textov
            result_text.insert(tk.END, f"Chyba pri analýze zmiešaných textov: {str(e)}\n\n")
    
        #nastavenie len pre čítanie
        result_text.config(state='disabled')
        
    #GUI pre podstránku s identifikáciou pomocou RegEx
    def show_regex_based(self):
        #premazanie obsahu
        self.clear_screen()
        
        #tlačidlo späť pre návrat na hlavnú stránku
        back_button = tk.Button(
            self.root,
            text="← Späť",
            command=self.create_main_screen,
            font=("Arial", 15)
        )
        back_button.place(x=20, y=20)
        self.active_widgets.append(back_button)
        
        #nazov podstránky
        label = tk.Label(self.root, text="Identifikácia pomocou RegEx", font=("Arial", 24, "bold"))
        label.pack(pady=20)
        self.active_widgets.append(label)
        
        #textove pole na vloženie textu
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
    
    #GUI pre podstránku s identifikáciou pomocou part-of-speech tagging
    def show_post_based(self):
        #premazanie obsahu
        self.clear_screen()
        
        #tlačidlo späť pre návrat na hlavnú stránku
        back_button = tk.Button(
            self.root,
            text="← Späť",
            command=self.create_main_screen,
            font=("Arial", 15)
        )
        back_button.place(x=20, y=20)
        self.active_widgets.append(back_button)
        
        #nazov podstránky
        label = tk.Label(self.root, text="Identifikácia pomocou Part-of-speech tagging", font=("Arial", 24, "bold"))
        label.pack(pady=20)
        self.active_widgets.append(label)
        
        #textove pole na vloženie textu
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
    
    #GUI pre podstránku na porovnanie metod POST a RegEx
    def show_comparison(self):
        #premazanie obsahu
        self.clear_screen()
        
        #tlačidlo späť pre návrat na hlavnú stránku
        back_button = tk.Button(
            self.root,
            text="← Späť",
            command=self.create_main_screen,
            font=("Arial", 15)
        )
        back_button.place(x=20, y=20)
        self.active_widgets.append(back_button)
        
        #nazov podstránky
        label = tk.Label(self.root, text="Porovnanie identifikačných metód", font=("Arial", 24, "bold"))
        label.pack(pady=20)
        self.active_widgets.append(label)
        
        #informačný text
        info_label = tk.Label(
            self.root,
            text="Kliknutím na tlačidlo sa spustí porovnanie identifikácie definícií\nv medicínskych a zmiešaných textoch",
            font=("Arial", 14),
            justify=tk.CENTER
        )
        info_label.pack(pady=50)
        self.active_widgets.append(info_label)
        
        #tlačidlo pre spustenie porovnania metód
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
    app = DefinitionIdentificationApp(root)
    root.mainloop()