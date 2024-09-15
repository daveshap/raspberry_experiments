import anthropic
import random

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

def format_subtopic_prompt(params):
    with open('prompt_generate_subtopic.txt', 'r') as file:
        template = file.read()
    return template.format(**params)

def query_claude(api_key, prompt):
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    return message.content

def generate_subtopic(api_key, params):
    prompt = format_subtopic_prompt(params)
    print("Generated Prompt:")
    print(prompt)
    print("\n--- End of Prompt ---\n")
    response = query_claude(api_key, prompt)
    print("API Response:")
    print(response)
    print("\n--- End of API Response ---\n")
    
    # Extract the text from the TextBlock object
    if isinstance(response, list) and len(response) > 0:
        return response[0].text.strip()
    else:
        return "Error: Unexpected response format"

# Usage
with open('key.txt', 'r') as file:
    api_key = file.read().strip()

params = generate_question_parameters()
subtopic = generate_subtopic(api_key, params)

print(f"Main Topic: {params['main_topic']}")
print(f"Difficulty: {params['difficulty']}")
print(f"Problem Type: {params['problem_type']}")
print(f"Conceptual Connector: {params['conceptual_connector']}")
print(f"Generated Subtopic: {subtopic}")