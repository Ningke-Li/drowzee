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
    prolog_instance.consult("prolog_rules/geography.pl")  # 加载 Prolog 文件
    return prolog_instance



def transitive_inference(triples, new_fact_list):
    prolog = Prolog()
    key_list = [['contains_settlement', 'located_in_or_next_to_body_of_water'], 'shares_border_with']
    query_list = ['settlement_near_body_of_water(PlaceA, PlaceB, PlaceC)', 'indirectly_shares_border_with(PlaceA, PlaceB, PlaceC)']
    for idx, query in enumerate(query_list):
        selected_triples = [triple for triple in triples if triple['predicate'] in key_list[idx]]
        print(len(selected_triples))
        prolog = triples2prolog_facts(selected_triples, prolog)
        prolog = define_rules(prolog)
        if len(selected_triples) > 1000:
            selected_triples = random.sample(selected_triples, 1000)
        print(len(selected_triples))
        problem = query_list[idx]
        cnt = 0
        for soln in prolog.query(problem):
            if soln:
                new_fact = {
                    "category": "Geography and Places",
                    "reasoning": "Transitive Inference",
                    "PlaceA": soln['PlaceA'].strip("'"),
                    "subject": soln['PlaceB'].strip("'"),
                    "predicate": problem.split('(')[0],
                    "object": soln['PlaceC'].strip("'")
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
    key_list = ['capital_of', 'located_in_the_administrative_territorial_entity']
    query_list = ['country_of', 'administrative_territorial_entity_of']
    for idx, key in enumerate(key_list):
        selected_triples = [triple for triple in triples if triple['predicate'] == key]
        prolog = triples2prolog_facts(selected_triples, prolog)
        prolog = define_rules(prolog)
        if len(selected_triples) > 2000:
            num_extracted = random.randint(1000, 1500)
            selected_triples = random.sample(selected_triples, num_extracted)
        print(len(selected_triples))
        for triple in selected_triples:
            placea = triple['subject']
            problem = f'{query_list[idx]}(PlaceB, {placea}).'
            cnt = 0
            for soln in prolog.query(problem):
                if soln:
                    new_fact = {
                        "category": "Geography and Places",
                        "reasoning": "Inverse Function Inference",
                        "subject": soln['PlaceB'].strip("'"),
                        "predicate": problem.split('(')[0],
                        "object": placea.strip("'")
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
    key_list = [['k_ppen_climate_classification', 'heritage_designation']]
    query_list = ['similar_places']
    for idx, key in enumerate(key_list):
        selected_triples = [triple for triple in triples if triple['predicate'] in key]
        prolog = triples2prolog_facts(selected_triples, prolog)
        prolog = define_rules(prolog)
        if len(selected_triples) > 2000:
            num_extracted = random.randint(1500, 2000)
            selected_triples = random.sample(selected_triples, num_extracted)
        print(len(selected_triples))
        cnt = 0
        for triple in selected_triples:
            placea = triple['subject']
            for triple in random.sample(selected_triples, 100):
                placeb = triple['subject']
                if placea == placeb:
                    continue
                problem = f'{query_list[idx]}({placea}, {placeb}, Similarities)'
                
                for soln in list(prolog.query(problem)):
                    if len(soln["Similarities"]) > 0:
                        new_fact = {
                            "category": "Geography and Places",
                            "reasoning": "Inference Chain",
                            "subject": placea.strip("'"),
                            "predicate": problem.split('(')[0],
                            "object": placeb.strip("'"),
                            "similarity": [str(s).strip("'") for s in soln["Similarities"]]
                        }
                        print(new_fact)
                        new_fact_list.append(new_fact)
                        cnt += 1
                if cnt >= 100:
                    cnt = 0
                    break
    return new_fact_list


def negation_inference(triples, new_fact_list):
    prolog = Prolog()
    key_list = ['country']
    query_list = ['not_same_country']
    for idx, key in enumerate(key_list):
        selected_triples = [triple for triple in triples if triple['predicate'] == key]
        prolog = triples2prolog_facts(selected_triples, prolog)
        prolog = define_rules(prolog)
        if len(selected_triples) > 150:
            num_extracted = random.randint(50,100)
            selected_triples = random.sample(selected_triples, num_extracted)
        print(len(selected_triples))
        for triple in selected_triples:
            citya = triple['subject']
            problem = f'{query_list[idx]}({citya}, City2).'
            cnt = 0
            # print(len(list(prolog.query(problem)))>0)
            for soln in prolog.query(problem):
                if soln:
                    new_fact = {
                        "category": "Geography and Places",
                        "reasoning": "Negation Inference",
                        "subject": citya.strip("'"),
                        "predicate": problem.split('(')[0],
                        "object": soln['City2'].strip("'")
                    }
                    print(new_fact)
                    new_fact_list.append(new_fact)
                    cnt += 1 
            if cnt >= 10:
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
    print(len(new_fact_list))
    return new_fact_list


if __name__ == '__main__':
    # 创建Prolog实例
    prolog = Prolog()
    all_triples = [json.loads(line) for line in open('data/geography_related_triples.txt', 'r', encoding='utf-8').readlines()]
    new_fact_list = prolog_inference(all_triples, prolog)
    output_path = 'data/generation/geography_new_facts.txt'
    unique_new_fact_list = remove_duplicates(output_path, new_fact_list)
    print(len(unique_new_fact_list))