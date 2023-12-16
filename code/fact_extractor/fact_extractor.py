import os
import json
from pyswip import Prolog
from tqdm import tqdm
from datetime import datetime
import re

def escape_characters(input_string):
    # 替换的转义字符映射
    replacements = {
        "\\": "\\\\",  # 反斜杠
        "'": "\\\\'",     # 单引号
        "\"": "\\\"",   # 双引号
        "\n": "\\n",    # 换行符
        "\r": "\\r",    # 回车符
        "\t": "\\t",    # 制表符
        "\b": "\\b",    # 退格符
        "\f": "\\f"     # 换页符
    }

    # 遍历替换字典进行替换
    for key, value in replacements.items():
        input_string = input_string.replace(key, value)

    return input_string

def quote_if_starts_with_digit(s):
    s = re.sub(r'[^a-zA-Z0-9]', '_', s)
    # 检查字符串是否以数字开头
    if s and s[0].isdigit():
        return f'\'{s}\''  # 如果是，加上单引号
    return s  # 否则返回原字符串

def replace_special_characters(s):
    s = re.sub(r'[^a-zA-Z0-9]', '_', s)
    return s

def extract_related_triples(input_file, output_path):
    # 读取JSON文件
    extracted_triples = list()
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in tqdm(file.readlines()):
            try:
                json_data = json.loads(line)
                title = json_data['title']
                triples = json_data["triples"]
                # predicate_set = set()
                for triple in triples:
                    triple_dict = dict()
                    triple_dict['title'] = title
                    triple_dict['subject'] = f'\'{replace_special_characters(triple[0])}\''
                    
                    triple_dict['predicate'] = replace_special_characters(escape_characters(triple[1])).lower()
                    triple_dict['object'] = f'\'{replace_special_characters(triple[2])}\''
                    triple_dict['original_object'] = triple[2] 
                    extracted_triples.append(triple_dict)
            except json.JSONDecodeError:
                # 忽略无法解析的行
                continue
    with open(output_path, 'w', encoding='utf-8') as file:
        print(f"Writing {len(extracted_triples)} triples to {output_path}")
        for triple in extracted_triples:
            json.dump(triple, file, ensure_ascii=False)
            file.write('\n')
    # return extracted_triples
    unique_triples = set()
    all_triples = list()
    # 读取文件并去重
    with open(output_path, 'r') as file:
        for line in file:
            unique_triples.add(line.strip())

    for line in unique_triples:
        all_triples.append(json.loads(line))
    
    results = sorted(all_triples, key=lambda x: x['title'])
    
    # 写回文件
    with open(output_path, 'w') as file:
        for line in results:
            json.dump(line, file, ensure_ascii=False)
            file.write('\n')

    return results


if __name__ == '__main__':
    collection_list = ['culture', 'geography', 'history', 'people', 'society', 'tech', 'math', 'health', 'nature']
    for collection in collection_list:
        if not os.path.exists(f'data/{collection}_related_triples.txt'):    
            triples = extract_related_triples(f'data/collection/{collection}.txt', f'data/triples/{collection}_related_triples.txt')