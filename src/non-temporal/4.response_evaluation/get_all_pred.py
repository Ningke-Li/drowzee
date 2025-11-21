import json
from nltk.corpus import wordnet

def export_synonyms_to_json(output_file="utils/wordnet_synonyms.json"):
    synonyms_dict = {}

    for synset in wordnet.all_synsets():
        for lemma in synset.lemmas():
            word = lemma.name().lower()
            if word not in synonyms_dict:
                synonyms_dict[word] = set()
            for synonym in synset.lemmas():
                if synonym.name().lower() != word:  
                    synonyms_dict[word].add(synonym.name().lower())

    synonyms_dict = {word: list(synonyms) for word, synonyms in synonyms_dict.items()}
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(synonyms_dict, f, indent=4)
