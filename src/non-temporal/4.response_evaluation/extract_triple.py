import time
import json
import concurrent.futures
from openai import OpenAI
import os
import threading


def openai_query(input_prompt):
    client = OpenAI(
        api_key='api_key_here'
    )
    while True:
        try:
            result = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": f"Given the questions, please provide a comprehensive answer based on your knowledge and reasoning"}, 
                    {   
                        "role": "user", 
                        "content": input_prompt}
                    ], 
                temperature=0, 
                timeout=30,
                max_tokens=500
                )
            # print(result)
            generated_content = result.choices[0].message.content
            print("result ", generated_content)
            break
        except:
            import traceback
            traceback.print_exc()
            print('error; waiting ten seconds and resubmitting')
            time.sleep(3)
    return generated_content

output_lock = threading.Lock()
count_lock = threading.Lock()
save_threshold = 100 
count = 0  

def save_output_data(output_path):
    with output_lock:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        print(f"Intermediate output saved to {output_path}")

def run_single_evaluation(qa_pairs, output_path):
    global count
    knowledge_list = qa_pairs["knowledge"]
    if knowledge_list:
        knowledge_list = "\n".join(knowledge_list)
        input_prompt = f"""
        You are given a set of sentences. For each sentence, extract the main information in the form of a triple (subject, predicate, object). A triple consists of three components:
            Subject: The entity the sentence is about.
            Predicate: The action or relationship described in the sentence.
            Object: The entity that is affected by the action or relationship.
            Example:
            Sentence: "The cat sits on the mat."
            Triple: ("The cat", "sits on", "the mat")
            Now, extract the triples from the following sentences:{knowledge_list}
            Expected output:
            For each sentence, return the triple in the format ("subject", "predicate", "object"). Only return the Triple part.
        """
        
        generated_content = openai_query(input_prompt)
        qa_pairs["triples"] = generated_content

    with output_lock:
        output_data.append(qa_pairs)

    with count_lock:
        count += 1
        if count % save_threshold == 0:
            save_output_data(output_path)



import json
import re

def process_json(json_data):
    triple_pattern = re.compile(r'\(\s*"(.+?)"\s*,\s*"(.*?)"\s*,\s*"(.*?)"\s*\)')
    
    for item in json_data:
        triples_text = item.get("triples", "")
        matches = triple_pattern.findall(triples_text)
        item['triples'] = [list(match) for match in matches]
    
    return json_data


model_list = ['llama3.1_8b', 'llama3.2_3b']
for model in model_list:
    input_file = f"{model}_triples.json"
    output_data = []
    with open(input_file, 'r') as f:
        qa_pairs = json.load(f)

    processed_data = process_json(qa_pairs)
    processed_data.sort(key=lambda x: x['qid'])
    with open(f"{model}_triples.json", 'w') as f:
        json.dump(processed_data, f, indent=4)
