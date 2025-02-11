import anthropic
import os
from pathlib import Path
import glob

def read_task_representation_prompt():
    # You would need to create this file containing the prompt we just created
    with open('system_task_representation.md', 'r', encoding='utf-8') as f:
        return f.read()

def process_question(client, question_text, system_prompt):
    """Process a single question through Claude"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=0,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question_text
                    }
                ]
            }
        ]
    )
    
    # Extract just the XML content from the response
    response_text = message.content[0].text
    start_tag = "<task_representation>"
    end_tag = "</task_representation>"
    start_idx = response_text.find(start_tag)
    end_idx = response_text.find(end_tag) + len(end_tag)
    
    if start_idx == -1 or end_idx == -1:
        raise ValueError(f"Could not find task_representation tags in response: {response_text}")
    
    return response_text[start_idx:end_idx]

def main():
    # Set up paths
    base_path = Path('.')
    questions_dir = base_path / 'Questions'
    output_dir = base_path / 'step02_task_representation'
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Read the system prompt
    system_prompt = read_task_representation_prompt()
    
    # Initialize Anthropic client
    with open('key.txt', 'r', encoding='utf-8') as file:
        api_key = file.read().strip()
    client = anthropic.Anthropic(api_key=api_key)
    
    # Process each question file
    for question_file in questions_dir.glob('question_*.txt'):
        output_file = output_dir / question_file.name
        
        # Skip if output file already exists
        if output_file.exists():
            print(f"Skipping existing file: {output_file}")
            continue
        
        try:
            # Read the question
            with open(question_file, 'r', encoding='utf-8') as f:
                question_text = f.read().strip()
            
            # Process through Claude
            task_representation = process_question(client, question_text, system_prompt)
            
            # Save the output
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(task_representation)
            
            print(f"Processed: {question_file.name}")
            
        except Exception as e:
            print(f"Error processing {question_file.name}: {str(e)}")

if __name__ == "__main__":
    main()