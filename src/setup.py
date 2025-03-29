import os
import sys
import subprocess
import venv
from pathlib import Path

def main():
    print("Začínam inštaláciu projektu...")
    
    #kontrola, či je projekt správne naklonovaný
    required_files = ["requirements.txt", "README.md"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"CHYBA: Súbor {file} nebol nájdený. Uistite sa, že ste v koreňovom adresári projektu.")
            sys.exit(1)
    
    #vytvorenie venv
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        print(f"Vytváram virtuálne prostredie v {venv_dir}...")
        venv.create(venv_dir, with_pip=True)
    else:
        print(f"Virtuálne prostredie v {venv_dir} už existuje.")
    
    #určenie cesty k pip v závislosti od operačného systému
    if os.name == 'nt':  #windows
        pip_path = os.path.join(venv_dir, "Scripts", "pip")
        python_path = os.path.join(venv_dir, "Scripts", "python")
    else:  #unix/linux/macos
        pip_path = os.path.join(venv_dir, "bin", "pip")
        python_path = os.path.join(venv_dir, "bin", "python")
    
    #inštalácia závislostí
    print("Inštalujem závislosti z requirements.txt...")
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
    
    #stiahnutie a inštalácia modelov pre stanza
    print("Sťahujem slovenské jazykové modely pre Stanza...")
    subprocess.check_call([
        python_path, "-c", 
        "import stanza; stanza.download('sk')"
    ])
    
    #vytvorenie adresárov, ak neexistujú
    directories = [
        "results/post",
        "results/regex"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("\nInštalácia úspešne dokončená!")
    print("Aktivujte virtuálne prostredie príkazom:")
    if os.name == 'nt':  #windows
        print("    venv\\Scripts\\activate")
    else:  #unix/linux/macos
        print("    source venv/bin/activate")
    print("Potom môžete spustiť program príkazom:")
    print("    python src/main.py")

if __name__ == "__main__":
    main()