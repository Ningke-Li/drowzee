import json
import os
from tqdm import tqdm
from prompt_template import generate_qa_pairs
import re
'''
qid: Question ID; 
entityid: Wikidata ID; 
entity: Wikipedia title; 
category: entity category; 
reasoning: reasoning strategy used for question generation;
question: A generation question.
answer: Yes/No.
evidence: triples that contain important information for result confirmation extracted from Wikidata.
'''
dataset_format = {
    "qid": "",
    "entityid": "",
    "entity": "",
    "description": "",
    "category": "",
    "reasoning": "",
    "question": "",
    "answer": "",
    "evidence": []
}

new_predicate_list = ['common_author', 'predecessor', 'common_director', 'same_series', 'common_cast_member', 'common_screenwriter', 'similar_type', 'successor_style', 'original_work', 'not_male_character', 'indirectly_shares_border_with', 'not_same_country', 'administrative_territorial_entity_of', 'settlement_near_body_of_water', 'country_of', 'similar_places', 'parent', 'same_subclass_event', 'same_participant', 'child_of_father', 'child_of_mother', 'not_occurred_in', 'killer', 'strategically_important_location', 'compare_career', 'same_political_party', 'same_award_received', 'teacher', 'not_shared_worldview', 'same_country', 'not_a_member', 'found_person', 'includes_member', 'same_operating_system', 'similar_distributed_by', 'not_designed_by', 'used_in_platform', 'named_after_same_person', 'discover', 'influential_research', 'no_proved_by', 'same_health_specialty', 'not_genetically_associated', 'influenced_by_disease', 'similar_symptoms_and_signs', 'same_medical_examination', 'similar_drug_or_therapy_used_for_treatment', 'not_parent_body', 'same_minor_planet_group', 'same_asteroid_spectral_type', 'preceded_by']
predicate_list = ['author', 'followed_by', 'director', 'part_of_the_series', 'cast_member', 'screenwriter', 'genre', 'influenced_by', 'derivative_work', ['instance_of', 'sex_or_gender'], 'shares_border_with', 'country', 'located_in_the_administrative_territorial_entity', ['contains_settlement', 'located_near_the_body_of_water'], 'capital_of', ['k_ppen_climate_classification', 'heritage_designation'], 'child', 'part_of', 'participant', 'father', 'mother', 'location', 'killed_by', ['instance_of', 'location'], ['notable_work', 'position_held'], 'member_of_political_party', 'award_received', 'student', 'religion_or_worldview', 'country', 'member_of', 'founded_by', 'member_of', 'operating_system', 'distributed_by', 'designed_by', 'platform', 'named_after', 'discoverer_or_inventor', 'studied_by', 'proved_by', 'health_specialty', 'genetic_association', 'genetic_association', 'symptoms_and_signs', 'medical_examination', 'drug_or_therapy_used_for_treatment', 'parent_astronomical_body', 'minor_planet_group', 'asteroid_spectral_type', 'followed_by']


def read_wiki_file(file_path):
    wiki_data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in tqdm(file.readlines()):
            try:
                entity_info = json.loads(line)
                entity_id = entity_info['id']
                entity_title = entity_info['title']
                entity_description = entity_info['text'].split('\n')[0]  # 取第一句话
                wiki_data[entity_title] = {
                    'entityid': entity_id,
                    'entity': entity_title,
                    'description': entity_description,
                    'triples': entity_info['triples']
                }
            except json.JSONDecodeError:
                print(f"Error decoding line: {line}")
    return wiki_data

def extract_entities(fact):
    """ 提取所有可能的实体名 """
    entities = []
    for key, value in fact.items():
        if key not in ['category', 'reasoning', 'predicate']:
            if isinstance(value, list):
                entities.extend(value)
            else:
                entities.append(value)
    return list(set(entities))

def read_new_facts_file(file_path):
    new_facts = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in tqdm(file.readlines()):
            try:
                fact = json.loads(line)
                new_facts.append(fact)
            except json.JSONDecodeError:
                print(f"Error decoding line: {line}")
    return new_facts


def replace_special_characters(s):
    s = re.sub(r'[^a-zA-Z0-9]', '_', s)
    return s


def construct_dataset(wiki_file, new_facts_file):
    wiki_data = read_wiki_file(wiki_file)
    new_facts = read_new_facts_file(new_facts_file)

    dataset = []
    for fact in new_facts:
        # print(fact)
        entity_id_list = list()
        entities = extract_entities(fact)
        entity_description_list = list()
        evidence = list()
        new_predicate = fact['predicate']
        predicate = predicate_list[new_predicate_list.index(new_predicate)]
        if new_predicate == 'not_male_character':
            print(predicate)
        question, answer = generate_qa_pairs(fact, collection)
        for entity in entities:
            # print(entity)
            entity_info = wiki_data.get(entity)
            if entity_info:
                # print(entity_info)
                entity_id_list.append(entity_info['entityid'])
                entity_description_list.append(entity_info['description'])
                for triple in entity_info['triples']:
                    if (type(predicate) == list and (replace_special_characters(triple[1]) in predicate)) or (type(predicate) == str and (replace_special_characters(triple[1]) == predicate)):
                        evidence.append(triple)
        dataset_entry = {
            "entityid": entity_id_list,
            "entity": entities,
            "description": entity_description_list,
            "category": fact['category'],
            "reasoning": fact['reasoning'],
            "question": question,  # 使用 construct_question 函数生成
            "answer": answer,   # 需要确定答案
            "evidence": evidence
        }
        # print(dataset_entry)
        dataset.append(dataset_entry)

    return dataset

def add_incremental_id_to_dataset(dataset):
    for i, item in enumerate(dataset, start=1):
        item['qid'] = i
    return dataset

if __name__ == '__main__':
    # collection_list = ['culture', 'geography', 'history', 'people', 'society', 'tech', 'math', 'health', 'nature']
    collection_list = ['geography']
    for collection in collection_list:
        wiki_file = f'data/collection/{collection}.txt'
        new_facts_file = f'data/generation/cleaned_facts/{collection}_new_facts_filtered.txt'
        dataset = add_incremental_id_to_dataset(construct_dataset(wiki_file, new_facts_file))
        ordered_fields = ["qid", "entityid", "entity", "description", "category", "reasoning", "question", "answer", "evidence"]
        ordered_data = [{field: item[field] for field in ordered_fields} for item in dataset]
        # with open(f'dataset/{collection}_dataset.json', 'w', encoding='utf-8') as file:
        #     json.dump(ordered_data, file, ensure_ascii=False, indent=4)