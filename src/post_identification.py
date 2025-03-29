import stanza
from collections import defaultdict

def extract_definitions_stanza(text):
    #inicializácia Stanza pre slovenský jazyk
    nlp = stanza.Pipeline('sk', processors='tokenize,pos,lemma,depparse')
    
    #spracovanie textu
    doc = nlp(text)
    
    definitions = []
    seen_terms = set()
    
    #spracovanie viet
    for sentence in doc.sentences:
        #konverzia štruktúry vety
        words = {word.id: word for word in sentence.words}
        dependencies = defaultdict(list)
        for word in sentence.words:
            if word.head > 0:
                dependencies[word.head].append(word.id)
        
        #zoznam vzorcov na vyskúšanie
        patterns_to_try = [
            find_definition_pattern,
            find_means_pattern,
            find_defined_as_pattern,
            find_is_pattern,
            find_simple_is_pattern,
            find_noun_root_pattern
        ]
        
        for pattern_func in patterns_to_try:
            found = pattern_func(sentence, words, dependencies, seen_terms, definitions)
            if found:
                break
    
    return definitions

def find_definition_pattern(sentence, words, dependencies, seen_terms, definitions):
    #hladá vzor "Definícia X je Y"
    definition_word = None
    for word in sentence.words:
        if word.lemma.lower() == "definícia":
            definition_word = word
            break
            
    if definition_word:
        term_id = None
        for dep_id in dependencies[definition_word.id]:
            if words[dep_id].deprel == "nmod":
                term_id = dep_id
                break
                
        if term_id:
            verb_id = None
            for w_id, w in words.items():
                if w.lemma == "byť" and (w.head == 0 or w.head == definition_word.id):
                    verb_id = w_id
                    break
                    
            if verb_id:
                definition_id = None
                for w_id, w in words.items():
                    if w.head == verb_id and w.deprel == "nsubj" and w_id != definition_word.id:
                        definition_id = w_id
                        break
                
                if not definition_id:
                    for w_id, w in words.items():
                        if w.head == verb_id and w.id != definition_word.id and w.deprel not in ["punct", "aux", "cop"]:
                            definition_id = w_id
                            break
                        
                if definition_id:
                    term_lemma = words[term_id].lemma
                    if term_lemma == words[term_id].text and is_genitive(term_lemma):
                        term_lemma = get_lemma(term_lemma)
                    
                    definition = extract_text(definition_id, words, dependencies)
                    
                    if term_lemma and definition and term_lemma not in seen_terms:
                        seen_terms.add(term_lemma)
                        definitions.append((term_lemma, definition))
                        return True
    return False

def find_means_pattern(sentence, words, dependencies, seen_terms, definitions):
    #hladá vzor "X znamená Y"
    for word in sentence.words:
        if word.lemma == "znamenať" and word.deprel == "root":
            term_id = None
            definition_id = None
            
            for dep_id in dependencies[word.id]:
                if words[dep_id].deprel == "nsubj":
                    if not term_id:
                        term_id = dep_id
                    elif not definition_id:
                        definition_id = dep_id
            
            if term_id and not definition_id:
                for dep_id in dependencies[word.id]:
                    if words[dep_id].deprel in ["obj", "xcomp", "obl"]:
                        definition_id = dep_id
                        break
            
            if term_id and definition_id:
                term_lemma = words[term_id].lemma
                definition = extract_text(definition_id, words, dependencies)
                
                if term_lemma and definition and term_lemma not in seen_terms:
                    seen_terms.add(term_lemma)
                    definitions.append((term_lemma, definition))
                    return True
    return False

def find_defined_as_pattern(sentence, words, dependencies, seen_terms, definitions):
    #hladá vzor "X je definovaný ako Y"
    for word in sentence.words:
        if (word.lemma in ["definovať", "definícia"] or "defin" in word.lemma) and word.upos in ["ADJ", "VERB"]:
            term_id = None
            
            if word.deprel == "root":
                for dep_id in dependencies[word.id]:
                    if words[dep_id].deprel in ["nsubj", "nsubj:pass"]:
                        term_id = dep_id
                        break

            else:
                for w_id, w in words.items():
                    if w.head == word.head and w.deprel in ["nsubj", "nsubj:pass"]:
                        term_id = w_id
                        break
            
            if not term_id:
                continue
                
            ako_id = None
            for w_id, w in words.items():
                if w.lemma == "ako":
                    ako_id = w_id
                    break
                    
            if not ako_id:
                continue
                
            definition_head_id = None
            for w_id, w in words.items():
                if w.head == word.id and ako_id in dependencies[w_id]:
                    definition_head_id = w_id
                    break
            
            if not definition_head_id:
                for w_id, w in sorted(words.items()):
                    if w.head == ako_id:
                        definition_head_id = w_id
                        break
            
            if not definition_head_id:
                for w_id in sorted(words.keys()):
                    if w_id > ako_id:
                        definition_head_id = w_id
                        break
                
            if term_id and definition_head_id:
                term_lemma = words[term_id].lemma
                
                definition = extract_text(definition_head_id, words, dependencies)
                if definition.lower().startswith("ako "):
                    definition = definition[4:]
                
                if term_lemma and definition and term_lemma not in seen_terms:
                    seen_terms.add(term_lemma)
                    definitions.append((term_lemma, definition))
                    return True
    return False

def find_is_pattern(sentence, words, dependencies, seen_terms, definitions):
    #hladá všeobecný vzor "X je Y" s dvoma podmetmi
    for word in sentence.words:
        if word.lemma == "byť" and word.deprel == "root":
            subjects = []
            for dep_id in dependencies[word.id]:
                if words[dep_id].deprel in ["nsubj", "nsubj:pass"]:
                    subjects.append(dep_id)
            
            if len(subjects) < 2:
                continue
                
            term_id = subjects[0]
            definition_id = subjects[1]
            
            term_lemma = words[term_id].lemma
            definition = extract_text(definition_id, words, dependencies)
            
            if term_lemma and definition and term_lemma not in seen_terms:
                seen_terms.add(term_lemma)
                definitions.append((term_lemma, definition))
                return True
    return False

def find_simple_is_pattern(sentence, words, dependencies, seen_terms, definitions):
    #hladá jednoduchý vzor "X je Y"
    for word in sentence.words:
        if word.lemma == "byť" and word.deprel == "cop":
            root_id = word.head
            
            term_id = None
            for dep_id in dependencies[root_id]:
                if words[dep_id].deprel == "nsubj":
                    term_id = dep_id
                    break
            
            if term_id and root_id:
                term_lemma = words[term_id].lemma
                definition = words[root_id].text
                
                if term_lemma and definition and term_lemma not in seen_terms:
                    seen_terms.add(term_lemma)
                    definitions.append((term_lemma, definition))
                    return True
    return False

def find_noun_root_pattern(sentence, words, dependencies, seen_terms, definitions):
    #hladá vzor kde podstatné meno je koreňom vety a má podmet
    for word in sentence.words:
        if word.upos == "NOUN" and word.deprel == "root":
            term_id = None
            for dep_id in dependencies[word.id]:
                if words[dep_id].deprel == "nsubj":
                    term_id = dep_id
                    break
                    
            if term_id:
                for dep_id in dependencies[word.id]:
                    if words[dep_id].lemma == "byť" and words[dep_id].deprel == "cop":
                        term_lemma = words[term_id].lemma
                        definition = word.text
                        
                        if term_lemma and definition and term_lemma not in seen_terms:
                            seen_terms.add(term_lemma)
                            definitions.append((term_lemma, definition))
                            print(f"DEBUG: Našiel sa vzor s podstatným menom ako koreňom: {term_lemma} = {definition}")
                            return True
    return False

def is_genitive(word):
    genitive_endings = ['a', 'u', 'ov', 'í', 'ého', 'ej']
    for ending in genitive_endings:
        if word.endswith(ending):
            return True
    return False

def get_lemma(word):
    if word.endswith('a') and len(word) > 3:
        return word[:-1]
    elif word.endswith('u'):
        return word[:-1]
    elif word.endswith('ov'):
        return word[:-2]
    
    return word

def extract_text(root_id, words, dependencies):
    if not root_id or root_id not in words:
        return None
    
    def get_subtree_ids(node_id):
        subtree = [node_id]
        for child_id in dependencies[node_id]:
            subtree.extend(get_subtree_ids(child_id))
        return subtree
    
    subtree_ids = get_subtree_ids(root_id)
    
    sorted_ids = sorted(subtree_ids)
    
    text = ' '.join(words[word_id].text for word_id in sorted_ids)
    
    return text.strip()

def main():
    sample_text = (
        "Algoritmus je definovaný ako presne určený postup krokov, ktorý vedie k riešeniu konkrétneho problému. "
        "Pes je zviera. "
        "Definícia počítača je elektronické zariadenie, ktoré spracováva dáta. "
        "Fotosyntéza znamená proces, v ktorom rastliny vyrábajú kyslík. "
    )
    
    print("Hľadanie definícií pomocou Stanza...")
    definitions = extract_definitions_stanza(sample_text)
    
    if definitions:
        print("\nNájdené definície:")
        for term, definition in definitions:
            print(f"Termín: {term}")
            print(f"Definícia: {definition}")
            print("------")
    else:
        print("V texte nebola nájdená žiadna definícia")

if __name__ == "__main__":
    main()