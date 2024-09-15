import random
import requests
import json


random.seed()

def read_list_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Read lists from files
main_topics = read_list_from_file('list_main_topics.txt')
difficulties = read_list_from_file('list_difficulties.txt')
problem_types = read_list_from_file('list_problem_types.txt')
conceptual_connectors = read_list_from_file('list_conceptual_connectors.txt')


def generate_question_parameters():
    return {
        'main_topic': random.choice(main_topics),
        'difficulty': random.choice(difficulties),
        'problem_type': random.choice(problem_types),
        'conceptual_connector': random.choice(conceptual_connectors)
    }

# Example usage
#params = generate_question_parameters()
#print(f"Main Topic: {params['main_topic']}")
#print(f"Difficulty: {params['difficulty']}")
#print(f"Problem Type: {params['problem_type']}")
#print(f"Conceptual Connector: {params['conceptual_connector']}")

# TODO: Use these parameters to generate a subtopic or secondary topic
# TODO: Use all parameters to construct a prompt for question generation


def query_claude(api_key, prompt):
    url = "https://api.anthropic.com/v1/complete"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "claude-2.1",
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 300
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"
        

def format_subtopic_prompt(params):
    with open('prompt_generate_subtopic.txt', 'r') as file:
        template = file.read()
    
    return template.format(**params)

def generate_subtopic(api_key, params):
    prompt = format_subtopic_prompt(params)
    print("Generated Prompt:")
    print(prompt)
    print("\n--- End of Prompt ---\n")
    response = query_claude(api_key, prompt)
    print("Full API Response:")
    print(json.dumps(response, indent=2))
    print("\n--- End of API Response ---\n")
    if isinstance(response, dict) and 'completion' in response:
        return response['completion'].strip()
    else:
        return str(response)

# Usage
with open('key.txt', 'r') as file:
    api_key = file.read()

params = generate_question_parameters()
subtopic = generate_subtopic(api_key, params)

print(f"Main Topic: {params['main_topic']}")
print(f"Difficulty: {params['difficulty']}")
print(f"Problem Type: {params['problem_type']}")
print(f"Conceptual Connector: {params['conceptual_connector']}")
print(f"Generated Subtopic: {subtopic}")