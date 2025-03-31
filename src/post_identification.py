import stanza
import sys
from collections import defaultdict

#stanza nastavenie
try:
    nlp = stanza.Pipeline('sk', processors='tokenize,mwt,pos,lemma', verbose=False)
except Exception as e:
    print(f"Nepodarilo sa inicializovať Stanza pipeline: {e}", file=sys.stderr)
    print("Uistite sa, že slovenský model ('sk') je stiahnutý a dostupný.", file=sys.stderr)

#funkcia na extrakciu terminu a definície
def get_text_from_words(words, start_index, end_index):
    if not words or start_index >= end_index or start_index < 0 or end_index > len(words):
        return ""
    return " ".join([word.text for word in words[start_index:end_index]]).strip()

def extract_definitions_stanza(text):
    try:
        doc = nlp(text)
    except Exception as e:
        print(f"Chyba pri spracovaní textu pomocou Stanza: {e}", file=sys.stderr)
        return []
        
    try:
        found_definitions = []

        for sentence in doc.sentences:
            words = sentence.words
            num_words = len(words)

            for i, word in enumerate(words):
                #pattern 1.1: X je Y (striktná verzia)
                if word.lemma == 'byť' and word.upos == 'VERB' and word.feats and \
                'Person=3' in word.feats and 'Number=Sing' in word.feats and \
                'Tense=Pres' in word.feats and word.text.lower() == 'je':

                    if i > 0 and i < num_words - 1:
                        #definiendum = všetko pred 'je'
                        term = get_text_from_words(words, 0, i)
                        #definiens = všetko po 'je' (do konca vety)
                        definition = get_text_from_words(words, i + 1, num_words)

                        if term and definition:
                            found_definitions.append((term, definition))
                            
                #pattern 1.2: X je Y (zjednodušená verzia)
                elif word.text.lower() == 'je' and word.lemma == 'byť':
                    if i > 0 and i < num_words - 1:
                        #definiendum = všetko pred 'je'
                        term = get_text_from_words(words, 0, i)
                        #definiens = všetko po 'je' (do konca vety)
                        definition = get_text_from_words(words, i + 1, num_words)
                        
                        if term and definition:
                            found_definitions.append((term, definition))

                #pattern 2: Definícia X je Y
                if i == 0 and word.lemma == 'definícia' and word.upos == 'NOUN':
                    for j in range(i + 1, num_words):
                        if words[j].lemma == 'byť' and words[j].text.lower() == 'je':
                            #definiendum = slová medzi 'Definícia' a 'je'
                            term = get_text_from_words(words, i + 1, j)
                            #definiens = slová po 'je'
                            definition = get_text_from_words(words, j + 1, num_words)
                            if term and definition:
                                found_definitions.append((term, definition))
                                break

                #pattern 3: X je definovaný/á/é ako Y
                elif word.lemma == 'byť' and word.text.lower() == 'je' and i < num_words - 2:
                    next_word = words[i+1]
                    after_next_word = words[i+2]

                    if next_word.lemma == 'definovaný' and (next_word.upos == 'ADJ' or next_word.upos == 'VERB') \
                    and after_next_word.lemma == 'ako':
                        if i > 0 and i < num_words - 3:
                            #definiendum = všetko pred 'je'
                            term = get_text_from_words(words, 0, i)
                            #definiens = všetko po 'ako'
                            definition = get_text_from_words(words, i + 3, num_words)

                            if term and definition:
                                found_definitions.append((term, definition))

                #pattern 4: X sa definuje ako Y
                elif word.lemma == 'definovať' and word.upos == 'VERB' and word.feats and \
                    'Person=3' in word.feats and 'Tense=Pres' in word.feats:

                    if i > 0 and words[i-1].lemma == 'sa' and words[i-1].upos == 'PRON' \
                        and i < num_words - 1 and words[i+1].lemma == 'ako':

                        if i > 1 and i < num_words - 2:
                            #definiendum = všetko pred 'sa'
                            term = get_text_from_words(words, 0, i - 1)
                            #definiens = všetko po 'ako'
                            definition = get_text_from_words(words, i + 2, num_words)

                            if term and definition:
                                found_definitions.append((term, definition))

                #pattern 5: Definovaním X rozumieme Y
                elif word.lemma == 'rozumieť' and word.upos == 'VERB' and word.feats and \
                    'Person=1' in word.feats and 'Number=Plur' in word.feats and 'Tense=Pres' in word.feats:

                    if i > 1 and words[0].lemma == 'definovanie' and words[0].upos == 'NOUN' \
                        and words[0].feats and 'Case=Ins' in words[0].feats:
                        #definiendum = slová medzi "Definovaním" a "rozumieme"
                        term = get_text_from_words(words, 1, i)
                        #definiens = slová po "rozumieme"
                        definition = get_text_from_words(words, i + 1, num_words)

                        if term and definition:
                            found_definitions.append((term, definition))

                #pattern 6: X znamená Y
                elif word.lemma == 'znamenať' and word.upos == 'VERB' and word.feats and \
                    'Person=3' in word.feats and 'Number=Sing' in word.feats and 'Tense=Pres' in word.feats:

                    if i > 0 and i < num_words - 1:
                        #definiendum = všetko pred 'znamená'
                        term = get_text_from_words(words, 0, i)
                        #definiens = všetko po 'znamená'
                        definition = get_text_from_words(words, i + 1, num_words)

                        if term and definition:
                            found_definitions.append((term, definition))

                #pattern 7: Výraz X znamená Y
                if i == 0 and word.lemma == 'výraz' and word.upos == 'NOUN':
                    for j in range(i + 1, num_words):
                        if words[j].lemma == 'znamenať' and words[j].text.lower() == 'znamená':
                            #definiendum = slová medzi 'Výraz' a 'znamená'
                            term = get_text_from_words(words, i + 1, j)
                            #definiens = slová po 'znamená'
                            definition = get_text_from_words(words, j + 1, num_words)
                            if term and definition:
                                found_definitions.append((term, definition))
                                break

        #odstránenie duplikátov
        unique_defs = []
        seen = set()
        for term, definition in found_definitions:
            key = (term, definition)
            if key not in seen:
                unique_defs.append(key)
                seen.add(key)

        return unique_defs
        
    except Exception as e:
        print(f"Chyba pri identifikácii definícií: {e}", file=sys.stderr)
        return []
        
def main():
    text_s_definicami = """
    Pes je zviera.
    """

    print("\n--- Hľadanie definícií pomocou Stanza ---")
    najdene_definicie = extract_definitions_stanza(text_s_definicami)

    print(f"\nNájdených definícií: {len(najdene_definicie)}")
    for i, (term, definition) in enumerate(najdene_definicie):
        print(f"\nDefinícia č. {i+1}:")
        print(f"  Termín (Definiendum): '{term}'")
        print(f"  Definícia (Definiens): '{definition}'")

if __name__ == "__main__":
    main()