import re

def extract_definitions(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    patterns = [
        #priama definicia
        r'([\w\s\-]+?)\sje\s([\w\s\-,.()]+)',
        r'Definícia\s([\w\s\-]+?)\sje\s([\w\s\-,.()]+)',
        r'([\w\s\-]+?)\sje\sdefinovan[áýé]\sako\s([\w\s\-,.()]+)',
        #reflexivna konštrukcia
        r'([\w\s\-]+?)\ssa\sdefinuj[eú]\sako\s([\w\s\-,.()]+)',
        r'Definovaním\s([\w\s\-]+?)\srozumieme\s([\w\s\-,.()]+)',
        #sloveso
        r'([\w\s\-]+?)\sznamená\s+([\w\s\-,.()]+)',
        r'Výraz\s([\w\s\-]+?)\sznamená\s([\w\s\-,.()]+)'
    ]

    seen_terms = set()
    definitions = []

    for sentence in sentences:
        sentence = sentence.strip()
            
        for pattern in patterns:
            matches = re.findall(pattern, sentence, re.IGNORECASE)
            for match in matches:
                term = match[0].strip()
                definition = match[1].strip()
                
                if term not in seen_terms:
                    seen_terms.add(term)
                    definitions.append((term, definition))
                    break
            else:
                continue
            break
    
    return definitions

def main():
    sample_text = (
        "Algoritmus je definovaný ako presne určený postup krokov, ktorý vedie k riešeniu konkrétneho problému. "
        "Pes je zviera."
    )
    
    defs = extract_definitions(sample_text)
    
    if defs:
        for term, definition in defs:
            print(f"Termín: {term}")
            print(f"Definícia: {definition}")
            print("------")
    else:
        print("V texte nebola najdena žiadna definicia")

if __name__ == "__main__":
    main()