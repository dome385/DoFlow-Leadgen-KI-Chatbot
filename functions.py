import json
import os
import openai

# def add_complaint_to_table(complaint):
    

def create_assistant(api_key):
    assistant_file_path = 'assistant.json'

    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        # Upload the file containing information about the vacation rental
        file_response = openai.File.create(
            file=open("FeWo Infos.txt", "rb"),
            purpose='fine-tune'
        )
        file_id = file_response['id']

        # Save the file ID and use it in chat completions
        assistant_id = file_id

        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant_id}, file)
            print("Created a new assistant and saved the ID.")

    return assistant_id

def load_assistant_instructions(file_path):
    with open(file_path, 'r') as file:
        instructions = file.read()
    return instructions

def chat_with_assistant(api_key, messages):
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        functions=[{
            "name": "add_complaint_to_table",
            "description": """Fügt die Beschwerden von Gästen einer Tabelle hinzu.""",
            "parameters": {
                "type": "object",
                "properties": {}
            }
            
            
        }],
        function_call = "auto"
    )

    return response['choices'][0]['message']['content']
