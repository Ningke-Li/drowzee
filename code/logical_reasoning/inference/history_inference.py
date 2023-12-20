import os
import json
from pyswip import Prolog, Atom
from tqdm import tqdm
from datetime import datetime
import random

def add_prefix_if_starts_with_number(s):
    # 检查字符串是否以数字开头
    if s and s[0].isdigit():
        return "a_" + s
    elif s == 'length':
        return 'object_length'
    else:
        return s.strip('_')


def triples2prolog_facts(triples, prolog_instance):
    # 遍历三元组，转换成Prolog事实
    for triple in triples:
        subject = triple["subject"]
        predicate = add_prefix_if_starts_with_number(triple['predicate'])
        object_ = triple["object"]
        # 构造Prolog事实字符串
        fact = f"{predicate}({subject}, {object_})"
        # 告诉Prolog这个事实
        prolog_instance.assertz(fact)
    return prolog_instance

def define_rules(prolog_instance):
    prolog_instance.consult("prolog_rules/history.pl")  # 加载 Prolog 文件
    return prolog_instance



def transitive_inference(triples, new_fact_list):
    prolog = Prolog()
    key_list = ['part_of', 'participant']
    query_list = ['same_subclass_event(EventA, EventB).', 'same_participant(EventA, EventB).']
    for idx, query in enumerate(query_list):
        selected_triples = [triple for triple in triples if triple['predicate'] == key_list[idx]]
        prolog = triples2prolog_facts(selected_triples, prolog)
        prolog = define_rules(prolog)
        print(len(selected_triples))
        if len(selected_triples) > 1000:
            selected_triples = random.sample(selected_triples, 1000)
        print(len(selected_triples))
        
        problem = query_list[idx]
        cnt = 0
        for soln in prolog.query(problem):
            if soln:
                new_fact = {
                    "category": "History and Events",
                    "reasoning": "Transitive Inference",
                    "subject": soln['EventA'].strip("'"),
                    "predicate": query.split('(')[0],
                    "object": soln['EventB'].strip("'")
                }
                print(new_fact)
                new_fact_list.append(new_fact)
                cnt += 1
                if cnt >= 10000:
                    cnt = 0
                    break
    print(len(new_fact_list))
    return new_fact_list


def inverse_inference(triples, new_fact_list):
    prolog = Prolog()
    key_list = ['killed_by', 'child', 'mother', 'father']
    query_list = ['killer', 'parent', 'child_of_mother', 'child_of_father']
    for idx, key in enumerate(key_list):
        selected_triples = [triple for triple in triples if triple['predicate'] == key]
        prolog = triples2prolog_facts(selected_triples, prolog)
        prolog = define_rules(prolog)
        if len(selected_triples) > 2000:
            num_extracted = random.randint(1000, 1500)
            selected_triples = random.sample(selected_triples, num_extracted)
        print(len(selected_triples))
        for triple in selected_triples:
            persona = triple['subject']
            problem = f'{query_list[idx]}(PersonB, {persona}).'
            cnt = 0
            for soln in prolog.query(problem):
                if soln:
                    new_fact = {
                        "category": "History and Events",
                        "reasoning": "Inverse Function Inference",
                        "subject": soln['PersonB'].strip("'"),
                        "predicate": problem.split('(')[0],
                        "object": persona.strip("'")
                    }
                    print(new_fact)
                    new_fact_list.append(new_fact)
                    cnt += 1
                    if cnt >= 10000:
                        cnt = 0
                        break
    return new_fact_list


def chain_inference(triples, new_fact_list):
    prolog = Prolog()
    key_list = [['instance_of', 'location']]
    query_list = ['strategically_important_location']
    for idx, key in enumerate(key_list):
        selected_triples = [triple for triple in triples if triple['predicate'] in key]
        prolog = triples2prolog_facts(selected_triples, prolog)
        prolog = define_rules(prolog)
        if len(selected_triples) > 2000:
            num_extracted = random.randint(1000, 1500)
            selected_triples = random.sample(selected_triples, num_extracted)
        print(len(selected_triples))
        for triple in selected_triples:
            placea = triple['subject']
            problem = f'{query_list[idx]}(Battle1, Battle2, Location).'
            cnt = 0
            for soln in prolog.query(problem):
                if soln:
                    new_fact = {
                        "category": "History and Events",
                        "reasoning": "Inference Chain",
                        "subject": [soln['Battle1'].strip("'"), soln['Battle2'].strip("'")],
                        "predicate": problem.split('(')[0],
                        "object": soln['Location'].strip("'")
                    }
                    print(new_fact)
                    new_fact_list.append(new_fact)
                    cnt += 1
                    if cnt >= 10000:
                        cnt = 0
                        break
    return new_fact_list


def negation_inference(triples, new_fact_list):
    prolog = Prolog()
    key_list = ['location']
    query_list = ['not_occurred_in']
    for idx, key in enumerate(key_list):
        selected_triples = [triple for triple in triples if triple['predicate'] in key]
        location_list = list(set([triple['object'] for triple in selected_triples]))
        prolog = triples2prolog_facts(selected_triples, prolog)
        prolog = define_rules(prolog)
        print(len(selected_triples))
        cnt = 0
        for triple in selected_triples:
            event = triple['subject']
            for location in random.sample(location_list, 5):
                problem = f'{query_list[idx]}({event}, {location})'
                # print(problem)
                if len(list(prolog.query(problem))) > 0:
                    new_fact = {
                        "category": "History and Events",
                        "reasoning": "Negation Inference",
                        "subject": event.strip("'"),
                        "predicate": problem.split('(')[0],
                        "object": location.strip("'")
                    }
                    print(new_fact)
                    new_fact_list.append(new_fact)
                    cnt += 1
            if cnt >= 50:
                cnt = 0
                break    
    return new_fact_list


def remove_duplicates(output_path, new_fact_list):
    unique_triples = set()
    all_triples = list()
    unique_triples = set(json.dumps(data) for data in new_fact_list)
    new_triples = [json.loads(s) for s in unique_triples]
    with open(output_path, 'w', encoding='utf-8') as file:
        for fact in new_triples:
            # print(fact)
            json.dump(fact, file, ensure_ascii=False)
            file.write('\n')

    return unique_triples


def prolog_inference(all_triples, prolog):
    new_fact_list = list()
    triples = all_triples
    new_fact_list = transitive_inference(triples, new_fact_list)
    new_fact_list = inverse_inference(triples, new_fact_list)
    new_fact_list = chain_inference(triples, new_fact_list)
    new_fact_list = negation_inference(triples, new_fact_list)
    return new_fact_list


if __name__ == '__main__':
    # 创建Prolog实例
    prolog = Prolog()
    all_triples = [json.loads(line) for line in open('data/history_related_triples.txt', 'r', encoding='utf-8').readlines()]
    new_fact_list = prolog_inference(all_triples, prolog)
    output_path = 'data/generation/history_new_facts.txt'
    unique_new_fact_list = remove_duplicates(output_path, new_fact_list)
    print(len(unique_new_fact_list))
    