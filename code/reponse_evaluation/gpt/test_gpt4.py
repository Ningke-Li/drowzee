import openai
import time
import json
import concurrent.futures
import random
def openai_query(input_prompt):
    """
    :param input_prompt: a string of input prompt
    """

    openai.api_key = YOUR_API_KEY

    while True:
        try:
            # starttime = time.time()
            result = openai.ChatCompletion.create(model="gpt-4", messages=[ {"role": "system", "content": "Answer the question with your knowledge and reasoning power."}, {"role": "user", "content": input_prompt}], temperature=0, request_timeout=8,max_tokens=500)
            generated_content = result['choices'][0]['message']['content']
            # endtime = time.time()
            print("result ", generated_content)
            break
        except:
            import traceback
            traceback.print_exc()
            print('error; waiting ten seconds and resubmitting')
            time.wait(10)
    return generated_content

def openai_query_multi_turn(input_prompt):
    """
    :param input_prompt: a string of input prompt
    """
    generated_content_list = []
    openai.api_key = YOUR_API_KEY
    openai.api_base = "https://api.openai.com/v1/completions"
    for i in range(5):
        while True:
            try:
                result = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[ {"role": "system", "content": "Answer the question with your knowledge and reasoning power."}, {"role": "user", "content": input_prompt}], temperature=0, request_timeout=15,max_tokens=500)
                generated_content = result['choices'][0]['message']['content']
                
                print("result ", generated_content)
                break
            except:
                import traceback
                traceback.print_exc()
                print('error; waiting ten seconds and resubmitting')
        generated_content_list.append(generated_content)
    return generated_content_list

def run_single_evaluation(qa_pairs):
    # description = qa_pairs["description"]
    question = qa_pairs["question"]
    input_prompt = f"""
        Now given the question: '{question}', please provide an answer with ONLY Yes/No and show your reasoning process in the answer.
        The answer format should be: Yes, because .../No, because ... Other format of answers are strictly forbidden.
        NEVER answer with 'I don't know' or 'As an AI, I don't...' and so on.
    """
    # print(input_prompt)
    generated_content = openai_query(input_prompt)
    # generated_content = openai_query_multi_turn(input_prompt)
    qa_pairs["llm_answer"] = generated_content
    # qa_pairs["generation_time"] = generation_time
    output_data.append(qa_pairs)


output_data = []

collection_list = ['culture', 'geography', 'history', 'people', 'society', 'tech', 'math', 'health', 'nature']
for collection in collection_list:
    question_data = json.load(open(f'data/categorized/{collection}_dataset.json', 'r'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(run_single_evaluation, question_data)

    with open(f'res/gpt-4/{collection}.json', 'w') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
