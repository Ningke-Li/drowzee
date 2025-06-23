import json

def remove_duplicates_by_entity(input_file):
    # 打开并读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 用于存储唯一的实体
    seen_entities = set()
    unique_data = []

    # 遍历数据，检查entity字段并去重
    for item in data:
        entity = item.get('entity')
        if entity and entity not in seen_entities:
            unique_data.append(item)
            seen_entities.add(entity)
    
    # 将去重后的数据写回原始文件
    with open(input_file, 'w', encoding='utf-8') as file:
        json.dump(unique_data, file, ensure_ascii=False, indent=4)

# 使用示例
domain_list = ['culture', 'geography', 'history', 'health', 'math', 'nature', 'people', 'religion', 'society', 'tech']
for domain in domain_list:
    input_file = f'{domain}_useful_entities.json'
    remove_duplicates_by_entity(input_file)

    print(f"Processed file has been saved back to {input_file} with duplicates removed.")
