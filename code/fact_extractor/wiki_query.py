import requests
import json
import os
from tqdm import tqdm
from SPARQLWrapper import SPARQLWrapper, JSON

def query_wikidata_entity_id(title):
    # 执行SPARQL查询，返回entity ID
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
    SELECT ?item WHERE {
      ?item rdfs:label "%s"@en.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """ % title

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if len(results["results"]["bindings"]) == 0:
        return ''
    for result in results["results"]["bindings"]:
        return result["item"]["value"].split('/')[-1]

def query_wikidata_properties(entity_id):
    # 执行SPARQL查询，返回entity property/propertyLabel/value/valueLabel
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
    SELECT ?property ?propertyLabel ?value ?valueLabel WHERE {
        wd:%s ?p ?statement .
        ?statement ?ps ?value .
        ?property wikibase:claim ?p.
        ?property wikibase:statementProperty ?ps.
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        """ % entity_id
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    properties = []
    if len(results["results"]["bindings"]) == 0:
        return properties
    for result in results["results"]["bindings"]:
        properties.append({
            "property": result["property"]["value"],
            "propertyLabel": result["propertyLabel"]["value"],
            "value": result.get("value", {}).get("value"),
            "valueLabel": result.get("valueLabel", {}).get("value", "")
        })
    return properties


def construct_triples(title, properties):
    triples = []
    for prop in properties:
        triples.append((title, prop['propertyLabel'], prop['valueLabel']))
    return triples

def get_wikipedia_page_history(pageid):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "revisions",
        "pageids": pageid,
        "rvlimit": "1",
        "rvdir": "newer",  # 从最早的版本开始
        "rvprop": "timestamp",
        "format": "json"
    }

    response = requests_retry_session().get(url, params=params)
    if response.status_code == 200:
        if response.text:
            data = response.json()
            # 获取创建时间戳
            create_timestamp = data['query']['pages'][pageid]['revisions'][0]['timestamp']
    else:
        return '', '', []

    
    
    # 获取最新时间戳
    params['rvdir'] = 'older'  # 更改方向以获取最新的版本
    response = requests_retry_session().get(url, params=params)
    if response.status_code == 200:
        if response.text:
            data = response.json()
            latest_timestamp = data['query']['pages'][pageid]['revisions'][0]['timestamp']
    else:
        return '', '', []
    

    # 获取页面类别
    params_category = {
        "action": "query",
        "prop": "categories",
        "pageids": pageid,
        "format": "json"
    }

    category_response = requests_retry_session().get(url, params=params_category)
    if category_response.status_code == 200:
        if category_response.text:
            category_data = category_response.json()
            categories = [cat['title'] for cat in category_data['query']['pages'][pageid]['categories']]
    else:
        return '', '', []
    
    return create_timestamp, latest_timestamp, categories
def get_entity_categories(entity_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
    SELECT ?instanceOf ?instanceOfLabel WHERE {
      wd:%s wdt:P31 ?instanceOf .
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """ % entity_id

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    categories = []
    for result in results["results"]["bindings"]:
        categories.append({
            "instance_of": result.get("instanceOfLabel", {}).get("value", "")
        })
    return categories

def process_folder(input_folder, output_folder):
    files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    for i, filename in enumerate(tqdm(files, desc="Processing files")):
        input_file_path = os.path.join(input_folder, filename)
        process_json_file(input_file_path, output_folder, i+6)

def process_json_file(input_file, output_folder, index):
    output_file_number = 1
    output_file = open(os.path.join(output_folder, f'output_{index}_{output_file_number}.txt'), 'w', encoding='utf-8')
    
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)

            title = data['title']
            entity_id = query_wikidata_entity_id(title)
            if entity_id == '':
                continue
            properties = query_wikidata_properties(entity_id)
            if properties == []:
                continue
            triples = construct_triples(title, properties)
            page_id = data['id']
            # creation_timestamp, latest_timestamp, categories = get_wikipedia_page_history(page_id)

            # 更新JSON
            data.update({
                "entity_id": entity_id,
                "properties": properties,
                "triples": triples,
                "categories": categories,
                "creation_timestamp": creation_timestamp,
                "latest_timestamp": latest_timestamp
            })

            json.dump(data, output_file, ensure_ascii=False)
            output_file.write('\n')

            if output_file.tell() >= 50 * 1024 * 1024:  # 检查文件大小
                output_file.close()
                output_file_number += 1
                output_file = open(os.path.join(output_folder, f'output_{index}_{output_file_number}.txt'), 'w', encoding='utf-8')

    output_file.close()


# def thread_function(filename, input_folder, output_folder, output_suffix):
#     file_path = os.path.join(input_folder, filename)
#     output_folder_path = os.path.join(output_folder, f"output_{output_suffix}")
#     if not os.path.exists(output_folder_path):
#         os.makedirs(output_folder_path)
#     process_json_file(file_path, output_folder_path)


# def process_folder(input_folder, output_folder):
#     filenames = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
#     threads = []

#     for i, filename in enumerate(tqdm(filenames, desc="Processing files")):
#         thread = threading.Thread(target=thread_function, args=(filename, input_folder, output_folder, i))
#         thread.start()
#         threads.append(thread)

#     # 等待所有线程完成
#     for thread in threads:
#         thread.join()


if __name__ == '__main__':
    input_folder = 'data/wiki/wiki_data/useful_wiki'
    output_folder = 'data/wiki/wiki_triples'
    process_folder(input_folder, output_folder)
    