import anthropic
import random
import time
import os
from datetime import datetime


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

def format_subtopic_prompt(params):
    with open('prompt_generate_subtopic.txt', 'r') as file:
        template = file.read()
    return template.format(**params)

def format_question_prompt(params):
    with open('prompt_generate_question.txt', 'r') as file:
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
    response = query_claude(api_key, prompt)
    
    if isinstance(response, list) and len(response) > 0:
        return response[0].text.strip()
    else:
        return response.strip()  # Changed to handle string response

def generate_question(api_key, params):
    prompt = format_question_prompt(params)
    response = query_claude(api_key, prompt)
    
    if isinstance(response, list) and len(response) > 0:
        return response[0].text.strip()
    else:
        return response.strip()  # Changed to handle string response

def generate_full_question(api_key):
    params = generate_question_parameters()
    subtopic = generate_subtopic(api_key, params)
    
    params['subtopic'] = subtopic
    question = generate_question(api_key, params)
    
    return {
        'main_topic': params['main_topic'],
        'difficulty': params['difficulty'],
        'problem_type': params['problem_type'],
        'conceptual_connector': params['conceptual_connector'],
        'subtopic': subtopic,
        'question': question
    }

def save_question_and_log(question_data, subtopic_prompt, question_prompt):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"sample_{timestamp}_{question_data['main_topic'].replace(' ', '_')}.txt"
    
    # Save question
    os.makedirs('questions', exist_ok=True)
    with open(os.path.join('questions', filename), 'w') as file:
        file.write(question_data['question'])
    
    # Save log
    os.makedirs('log', exist_ok=True)
    with open(os.path.join('log', filename), 'w') as file:
        file.write(f"Main Topic: {question_data['main_topic']}\n")
        file.write(f"Difficulty: {question_data['difficulty']}\n")
        file.write(f"Problem Type: {question_data['problem_type']}\n")
        file.write(f"Conceptual Connector: {question_data['conceptual_connector']}\n")
        file.write(f"Subtopic: {question_data['subtopic']}\n\n")
        file.write("Subtopic Prompt Template:\n")
        file.write(subtopic_prompt + "\n\n")
        file.write("Question Prompt Template:\n")
        file.write(question_prompt + "\n\n")
        file.write("Generated Question:\n")
        file.write(question_data['question'])

# Main execution
with open('key.txt', 'r') as file:
    api_key = file.read().strip()

with open('prompt_generate_subtopic.txt', 'r') as file:
    subtopic_prompt_template = file.read()

with open('prompt_generate_question.txt', 'r') as file:
    question_prompt_template = file.read()

num_questions = 5  # Change this to the number of questions you want to generate

for i in range(num_questions):
    print(f"Generating question {i+1}/{num_questions}")
    question_data = generate_full_question(api_key)
    save_question_and_log(question_data, subtopic_prompt_template, question_prompt_template)
    print(f"Main Topic: {question_data['main_topic']}")
    print(f"Subtopic: {question_data['subtopic']}")
    print(f"Question: {question_data['question']}")
    print("\n---\n")
    time.sleep(2)  # Add a delay to avoid hitting API rate limits

print("Question generation complete. Check the 'questions' and 'log' folders for output.")