import anthropic
import json
import random
import os
from pathlib import Path

# Set up paths
base_path = Path('.')
system_prompt_path = base_path / 'system_question_generator.md'
categories_path = base_path / 'question_categories.json'
words_path = base_path / 'English_Words_Long.txt'
output_dir = base_path / 'Questions'

# Create output directory if it doesn't exist
output_dir.mkdir(exist_ok=True)

# Read system prompt
with open(system_prompt_path, 'r') as f:
    system_prompt = f.read()

# Read word list
with open(words_path, 'r') as f:
    word_list = [word.strip() for word in f.readlines() if word.strip()]

# Read categories
categories = []
with open(categories_path, 'r') as f:
    for line in f:
        categories.append(json.loads(line)['category'])

def extract_solution(response_text):
    """Extract text between <Solution> tags"""
    start = response_text.find('<Solution>') + len('<Solution>')
    end = response_text.find('</Solution>')
    if start == -1 or end == -1:
        return None
    return response_text[start:end].strip()

def query_claude(client, category, random_words):
    """Make API call to Claude with proper message structure"""
    user_input = f"Category: {category}\nContext words: {' '.join(random_words)}"
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=0.2,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_input
                    }
                ]
            }
        ]
    )
    
    # Handle the response object
    if hasattr(message.content, 'text'):
        return message.content.text
    elif isinstance(message.content, list) and len(message.content) > 0:
        return message.content[0].text
    else:
        return str(message.content)

def main():
    # Initialize Anthropic client
    with open('key.txt', 'r') as file:
        api_key = file.read().strip()
    client = anthropic.Anthropic(api_key=api_key)

    
    # Process each category
    for i, category in enumerate(categories):
        # Select 5-10 random words
        num_words = random.randint(5, 10)
        random_words = random.sample(word_list, num_words)
        
        # Get response from Claude
        response = query_claude(client, category, random_words)
        
        # Extract solution
        solution = extract_solution(response)
        
        if solution:
            # Save to file
            output_file = output_dir / f'question_{i+1}.txt'
            with open(output_file, 'w') as f:
                f.write(solution)
            
            print(f"Generated question {i+1} for category: {category[:50]}...")
        else:
            print(f"Failed to generate question for category {i+1}")

if __name__ == "__main__":
    main()