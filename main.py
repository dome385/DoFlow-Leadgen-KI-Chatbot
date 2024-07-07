import os
from time import sleep
from packaging import version
from flask import Flask, request, jsonify
import openai
import functions

# Check OpenAI version is correct
required_version = version.parse("0.28.0")

  # Check OpenAI version
current_version = version.parse(openai.__version__)
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
if current_version < required_version:
    raise ValueError(f"Error: OpenAI version {openai.__version__} is less than the required version 1.1.1")
else:
    print("OpenAI version is compatible.")

# Start Flask app
app = Flask(__name__)

# Init client
openai.api_key = OPENAI_API_KEY  # should use env variable OPENAI_API_KEY in secrets (bottom left corner)

# Load assistant instructions from file
assistant_instructions = functions.load_assistant_instructions('FeWo Infos.txt')

# Start conversation thread
@app.route('/start', methods=['GET'])
def start_conversation():
    print("Starting a new conversation...")  # Debugging line
    system_message = {
        "role": "system",
        "content": assistant_instructions
    }
    thread_response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[system_message]
    )
    thread_id = thread_response['id']
    print(f"New thread created with ID: {thread_id}")  # Debugging line
    return jsonify({"thread_id": thread_id})

# Generate response
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    thread_id = data.get('thread_id')
    user_input = data.get('message', '')

    if not thread_id:
        print("Error: Missing thread_id")  # Debugging line
        return jsonify({"error": "Missing thread_id"}), 400

    print(f"Received message: {user_input} for thread ID: {thread_id}")  # Debugging line

    # Retrieve previous messages to maintain context
    messages = [
        {"role": "system", "content": assistant_instructions},
        {"role": "user", "content": user_input}
    ]

    # Generate response from the Assistant
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages
    )

    assistant_response = response['choices'][0]['message']['content']

    print(f"Assistant response: {assistant_response}")  # Debugging line
    return jsonify({"response": assistant_response})

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

