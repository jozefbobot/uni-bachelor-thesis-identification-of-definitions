import tkinter as tk

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
        print(f"Spouštím Regex identifikaci textu: {text}")
    
    def run_stanza_identification(self):
        text = self.text_field.get("1.0", "end-1c")
        print(f"Spouštím Stanza identifikaci textu: {text}")
        
    def run_comparison(self):
        text = self.text_field.get("1.0", "end-1c")
        print(f"Spouštím porovnanie identifikačných metód na textu: {text}")
    
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
        
        #textove pole
        self.text_field = tk.Text(self.root, width=55, height=15, font=("Arial", 20))
        self.text_field.pack(pady=10)
        self.active_widgets.append(self.text_field)
        
        #tlačidlo pre spustenie porovnania
        identify_button = tk.Button(
            self.root,
            text="Porovnať",
            command=self.run_comparison,
            font=("Arial", 24),
            width=15,
            height=1
        )
        identify_button.pack(pady=20)
        self.active_widgets.append(identify_button)

if __name__ == "__main__":
    root = tk.Tk()
    app = DefinitionApp(root)
    root.mainloop()