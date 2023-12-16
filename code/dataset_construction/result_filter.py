import json
import os
from tqdm import tqdm

def update_json_line(line, replace_dict):
    data = json.loads(line)
    for key, value in data.items():
        if type(value) == str and value in replace_dict.keys():
            data[key] = replace_dict[value]
        elif type(value) == list:
            for i in range(len(value)):
                if value[i] in replace_dict.keys():
                    value[i] = replace_dict[value[i]]
            data[key] = value
    return json.dumps(data, ensure_ascii=False)

def punctuation_filter(ground_path, input_path, output_path):
    ground_dict = dict()
    with open(ground_path, 'r', encoding='utf-8') as file:
        for line in tqdm(file.readlines()):
            try:
                info_list = line.split('", "')
                title, subject, object_, original_object = '', '', '', ''
                for info in info_list:
                    # print(info)
                    if info.startswith('{"title'):
                        title = info.split('": "')[1].strip("'")
                        
                    elif info.startswith('subject":'):
                        subject = info.split('": "')[1].strip("'")
                    elif info.startswith('object'):
                        object_ = info.split('": "')[1].strip("'")
                        # print(object_)
                    elif info.startswith('original_object'):
                        original_object = info.split('": "')[1].strip('}"\n').strip("'")
                if title and subject and object_ and original_object:
                    # print(title, subject, object_, original_object)
                    if subject not in ground_dict.keys():
                        ground_dict[subject] = title
                    elif object_ not in ground_dict.keys():
                        ground_dict[object_] = original_object  
            except json.JSONDecodeError:
                # 忽略无法解析的行
                continue
    print(len(ground_dict))
    # new_fact_list = list()
    with open(input_path, 'r', encoding='utf-8') as f2:
        for fact_line in tqdm(f2.readlines()):
            try:
                updated_line = update_json_line(fact_line, ground_dict)
                with open(output_path, 'a', encoding='utf-8') as outfile:
                    outfile.write(updated_line + '\n')
            except json.JSONDecodeError:
                # 忽略无法解析的行
                continue
    # with open(output_path, 'w', encoding='utf-8') as file:
    #     for fact in new_fact_list:
    #         json.dump(fact, file, ensure_ascii=False)
    #         file.write('\n')

if __name__ == '__main__':
    collection_list = ['nature']
    for collection in collection_list:
        ground_path = f'data/{collection}_related_triples.txt'
        input_path = f'data/generation/{collection}_new_facts.txt'
        output_path = f'data/generation/cleaned_facts/{collection}_new_facts_filtered.txt'    
        punctuation_filter(ground_path, input_path, output_path)