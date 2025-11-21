import json
import spacy
from sentence_transformers import SentenceTransformer, util
import torch
import os
import shutil


nlp = spacy.load('en_core_web_md')
model = SentenceTransformer('all-MiniLM-L6-v2')

def check_reasoning_similarity(llm_reasoning, correct_reasoning):
    llm_embeddings = torch.tensor(model.encode(str(llm_reasoning)))
    correct_embeddings = torch.tensor(model.encode(correct_reasoning))
    similarity_scores = util.pytorch_cos_sim(llm_embeddings, correct_embeddings).item()
    adjusted_similarity = (similarity_scores + 1) / 2
    adjusted_similarity = min(adjusted_similarity, 1.0)
    return adjusted_similarity

def find_overlap_words_nlp(text1, text2):
    doc1 = nlp(text1.lower())
    doc2 = nlp(text2.lower())
    words1 = set(token.lemma_ for token in doc1 if not token.is_stop)
    words2 = set(token.lemma_ for token in doc2 if not token.is_stop)
    return words1.intersection(words2)

def find_overlap_words(text1, text2):
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    return words1.intersection(words2)

def remove_duplicate_triples(triples):
    unique_triples = []
    seen_pairs = set()
    for triple in triples:
        subject, predicate, obj = triple
        pair = (subject, predicate, obj)
        if pair not in seen_pairs:
            unique_triples.append(triple)
            seen_pairs.add(pair)
    return unique_triples

def remove_duplicate_fact_results(fact_results):
    unique_fact_results = []
    seen_pairs = set()
    for result in fact_results:
        pair = (result["evidence_subject"], result["triple_subject"], result["evidence_object"], result["triple_final_object"])
        if pair not in seen_pairs:
            unique_fact_results.append(result)
            seen_pairs.add(pair)
    return unique_fact_results

def remove_duplicate_reasoning_results(reasoning_results):
    unique_reasoning_results = []
    seen_pairs = set()
    for result in reasoning_results:
        pair = (result["evidence_predicate"], result["triple_predicate"])
        if pair not in seen_pairs:
            unique_reasoning_results.append(result)
            seen_pairs.add(pair)
    return unique_reasoning_results

def build_subject_object_map(triples):
    subject_object_map = {}
    for triple in triples:
        subject, _, obj = triple
        subject_object_map[subject] = obj
    return subject_object_map

def find_final_object(subject, subject_object_map, evi_object):
    current_obj = subject_object_map.get(subject)
    if find_overlap_words_nlp(current_obj, evi_object):
        return current_obj
    visited = set()  
    
    while current_obj and current_obj not in visited:
        visited.add(current_obj)
        
        matched_subject = None
        for sub, obj in subject_object_map.items():
            # print("current_obj:", current_obj)
            # print("sub:", sub)
            if find_overlap_words_nlp(current_obj, sub):  
                matched_subject = sub
                # print("matched_subject:", matched_subject)
                current_obj = obj
                break
        
        if not matched_subject: 
            break
    
    return current_obj

def find_related_objects(evidence_object, triples, max_depth=2):
    related_objects = set()
    
    def search(current_object, depth):
        if depth > max_depth:
            return
        for triple in triples:
            triple_subject, _, triple_object = triple
            if find_overlap_words(current_object, triple_object) or current_object in triple_subject:
                related_objects.add(triple_object)
                search(triple_object, depth + 1)

    search(evidence_object, 0)
    return related_objects


def calculate_similarity_with_final_object(evidence, triples):
    evidence = remove_duplicate_triples(evidence)
    triples = remove_duplicate_triples(triples)
    subject_object_map = build_subject_object_map(triples)
    fact_results = []
    reasoning_results = []
    # print(subject_object_map)
    for evi_triple in evidence:
        evi_subject, ev_predicate, evi_object = evi_triple
        # related_objects = find_related_objects(evi_object, triples)

        # for related_object in related_objects:
        #     similarity_score = check_reasoning_similarity(evi_object, related_object)
        #     fact_results.append({
        #         "evidence_subject": evi_subject,
        #         "triple_subject": "",
        #         "evidence_object": evi_object,
        #         "triple_final_object": related_object,
        #         "similarity_score": similarity_score
        #     })

        cnt = 0
        for triple in triples:
            # print(triple)
            triple_subject, triple_predicate, triple_object = triple
            subject_overlap_words = find_overlap_words(evi_subject, triple_subject)
            if 'couldn\'t' in triple_predicate or 'could not' in triple_predicate:
                reasoning_score = check_reasoning_similarity(ev_predicate, triple_predicate)
                reasoning_results.append({
                    "evidence_predicate": ev_predicate,
                    "triple_predicate": triple_predicate,
                    "similarity_score": reasoning_score
                })
            if (not subject_overlap_words) or (subject_overlap_words == {'the'}):
                continue
            # print("subject_overlap_words:", subject_overlap_words)
            final_object = find_final_object(triple_subject, subject_object_map, evi_object)
            # print(final_object)
            # if final_object == triple_object:
            #     object_overlap_words = find_overlap_words(evi_object, triple_object)
            # elif final_object != triple_object:
            #     print("final_object:", final_object)
            object_overlap_words = find_overlap_words(evi_object, final_object)
            
            if object_overlap_words:
                # final_object = find_final_object(triple_subject, subject_object_map)
                overlap_text = " ".join(object_overlap_words)
                similarity_score = check_reasoning_similarity(evi_object.lower(), overlap_text)
                fact_results.append({
                    "evidence_subject": evi_subject,
                    "triple_subject": triple_subject,
                    "evidence_object": evi_object,
                    "triple_final_object": final_object,
                    "similarity_score": similarity_score
                })
                reasoning_results.append({
                    "evidence_predicate": ev_predicate,
                    "triple_predicate": triple_predicate,
                    "similarity_score": 1.0
                })
                cnt += 1
            elif find_overlap_words(evi_object, triple_predicate):
                overlap_text = " ".join(find_overlap_words(evi_object, triple_predicate))
                similarity_score = check_reasoning_similarity(evi_object.lower(), overlap_text)
                fact_results.append({
                    "evidence_subject": evi_subject,
                    "triple_subject": triple_subject,
                    "evidence_object": evi_object,
                    "triple_final_object": triple_predicate,
                    "similarity_score": similarity_score
                })
                reasoning_results.append({
                    "evidence_predicate": ev_predicate,
                    "triple_predicate": triple_predicate,
                    "similarity_score": 1.0
                })
                cnt += 1
            elif find_overlap_words(evi_object, triple_subject):
                overlap_text = " ".join(find_overlap_words(evi_object, triple_subject))
                similarity_score = check_reasoning_similarity(evi_object.lower(), overlap_text)
                fact_results.append({
                    "evidence_subject": evi_subject,
                    "triple_subject": triple_subject,
                    "evidence_object": evi_object,
                    "triple_final_object": triple_subject,
                    "similarity_score": similarity_score
                })
                reasoning_results.append({
                    "evidence_predicate": ev_predicate,
                    "triple_predicate": triple_predicate,
                    "similarity_score": 1.0
                })
                cnt += 1
        # if cnt > 1:
        #     continue
        if cnt == 0:
            for triple in triples:
                triple_subject, _, triple_object = triple
                subject_overlap_words = find_overlap_words(evi_subject, triple_subject)
                if (not subject_overlap_words) or (subject_overlap_words == {'the'}):
                    continue
                similarity_score = check_reasoning_similarity(evi_object, triple_object)
                fact_results.append({
                    "evidence_subject": evi_subject,
                    "triple_subject": triple_subject,
                    "evidence_object": evi_object,
                    "triple_final_object": final_object,
                    "similarity_score": similarity_score
                })
                reasoning_score = check_reasoning_similarity(ev_predicate, triple_predicate)
                reasoning_results.append({
                    "evidence_predicate": ev_predicate,
                    "triple_predicate": triple_predicate,
                    "similarity_score": reasoning_score
                })
    return remove_duplicate_fact_results(fact_results), remove_duplicate_reasoning_results(reasoning_results)

# evidence = [
#     ["Burkitt Medal", "country", "United Kingdom"],
#     ["St Giles', Oxford", "country", "United Kingdom"]
# ]

# triples = [
#     ["The Burkitt Medal", "is awarded by", "the Royal College of Physicians in London, UK"],
#     ["St Giles'", "is", "a street in Oxford, Oxfordshire, UK"],
#     ["The Royal College of Physicians", "is located in", "the United Kingdom"],
#     ["Oxford, Oxfordshire", "is located in", "the United Kingdom"]
# ]

# results = calculate_similarity_with_final_object(evidence, triples)
# print(json.dumps(results, indent=4, ensure_ascii=False))
# print(sum(result["similarity_score"] for result in results) / len(results))

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    json_data = read_json('result_path.json')
    result_data = []  
    batch_size = 100  

    for i, sample in enumerate(json_data, 1):
        evidence = sample["evidence"]
        triples = sample["triples"]
        
        if evidence == [] or triples == [] or 'correctFact' not in sample.keys():  
            continue

        evidence = remove_duplicate_triples(evidence)
        triples = remove_duplicate_triples(triples)
        fact_results, reasoning_results = calculate_similarity_with_final_object(evidence, triples)
        sample["fact_similarity_results"] = fact_results
        sample["reasoning_similarity_results"] = reasoning_results
        sample["fact_score"] = sum(result["similarity_score"] for result in fact_results) / len(fact_results) if fact_results else 0.0
        sample["reasoning_score"] = sum(result["similarity_score"] for result in reasoning_results) / len(reasoning_results) if reasoning_results else 0.0
        result_data.append(sample)
        print(f"Processing Data {i} : {sample['correctFact'], sample['fact_score']}")

        if i % batch_size == 0:
            write_json(result_data, f"res/gpt_4o_part_{i // batch_size}.json")
            result_data = []  
    if result_data:
        write_json(result_data, f"res/gpt_4o_part_{(i // batch_size) + 1}.json")
    
if __name__ == "__main__":
    folder_path = 'res/gpt_4o'
    output_file = 'res/gpt_4o.json'

    json_files = [f for f in os.listdir(folder_path) if f.startswith('gpt_4o_part_') and f.endswith('.json')]
    merged_data = []

    for json_file in json_files:
        with open(os.path.join(folder_path, json_file), 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                del item['correctFact']
                del item['correctReasoning']
                merged_data.append(item)

    with open(output_file, 'w', encoding='utf-8') as output:
        json.dump(merged_data, output, ensure_ascii=False, indent=4)


    os.makedirs("res/gpt_4o", exist_ok=True)
    for json_file in json_files:
        shutil.move(os.path.join(folder_path, json_file), os.path.join("res/gpt_4o", json_file))
