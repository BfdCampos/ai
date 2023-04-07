import openai
import json
import os
from markdownify import markdownify as md

# Set up the OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

def read_large_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def format_response_to_markdown(response):
    markdown_sections = []
    
    for message in response['choices'][0]['message']['content']:
        if message['role'] == 'assistant':
            section_title = md(message['content'].strip())
            markdown_sections.append(f"## {section_title}\n")
    return "\n".join(markdown_sections)

def process_large_text_with_chatgpt(text, prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{text}\n{prompt}",
        temperature=0.5,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        stop=None,
    )
    
    return format_response_to_markdown(response)

def save_to_markdown_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    # Read the large text file
    input_file_path = "large_text_file.txt"
    large_text = read_large_text_file(input_file_path)
    
    # Set your desired prompt
    prompt = "Summarize the text into sections and titles."

    # Process the text with ChatGPT
    markdown_content = process_large_text_with_chatgpt(large_text, prompt)
    
    # Save the output to a markdown file
    output_file_path = "output.md"
    save_to_markdown_file(output_file_path, markdown_content)

    print(f"Output saved in {output_file_path}")

