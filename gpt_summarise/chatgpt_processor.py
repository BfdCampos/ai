import openai
import json
import os

# Set up the OpenAI API key
openai.api_key = ""

def split_text_into_chunks(text, chunk_size=5000):
    text_chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return text_chunks

def process_large_text_with_chatgpt(text, prompt):
    chunks = split_text_into_chunks(text)
    responses = []

    for chunk in chunks:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{prompt}\n{chunk}",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.25,
        )
        responses.append(response.choices[0].text.strip())

    return "\n".join(responses)

def summarize_to_bullet_points(summary, prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{prompt}\n{summary}",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def save_output_to_markdown(output, output_file_path):
    with open(output_file_path, "w") as f:
        f.write(output)

if __name__ == "__main__":
    input_file_path = "futpal_pitch_deck_discussion_apr_23.txt"
    prompt = "Summarise this transcript of a meeting into meeting notes. Meaning just return the main points made in the meeting related to the meeting content only, between people in a company into sections and titles."

    with open(input_file_path, "r") as f:
        large_text = f.read()

    summary = process_large_text_with_chatgpt(large_text, prompt)

    bullet_point_prompt = "Transform the following summary into a coherent list of bullet points highlighting the main points of the meeting:"
    bullet_point_summary = summarize_to_bullet_points(summary, bullet_point_prompt)

    input_file_path_list = input_file_path.split(".")
    output_file_path = f"{input_file_path_list[0]}_summary.md"

    save_output_to_markdown(bullet_point_summary, output_file_path)

    print(f"Output saved in {output_file_path}")

