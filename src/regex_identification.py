import re

def extract_definitions(text):
    #rozdelenie textu na vety
    sentences = re.split(r'(?<=[.!?])\s+', text)

    #vzory pre hladanie definicii
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

    #zoznam pre uz spracované terminy
    seen_terms = set()

    #zoznam pre nájdené definície
    definitions = []

    for sentence in sentences:
        #odstránenie medzier zo začiatku a konca vety
        sentence = sentence.strip()
        
        #prejdenie všetkých vzorov
        for pattern in patterns:
            #hľadanie zhody
            matches = re.findall(pattern, sentence, re.IGNORECASE)
            for match in matches:
                #extrakcia termínu a definície a odstránenie medzier
                term = match[0].strip()
                definition = match[1].strip()
                
                if term not in seen_terms:
                    #pridanie terminu a definicie do zoznamu ak ešte nebol spracovany
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
    
    definitions = extract_definitions(sample_text)
    
    if definitions:
        for term, definition in definitions:
            print(f"Termín: {term}")
            print(f"Definícia: {definition}")
            print("------")
    else:
        print("V texte nebola najdena žiadna definicia")

if __name__ == "__main__":
    main()