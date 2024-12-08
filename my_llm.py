import textwrap
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

def to_markdown(text):
    # Replace bold markers with HTML <strong> tags
    text = text.replace('**', '<strong>').replace('__', '<strong>')

    # Close the bold tags correctly
    text = text.replace('<strong>', '<strong>').replace('</strong>', '</strong>')

    # Replace bullet points with HTML <ul> and <li> tags
    #text = text.replace('* ', '<li>').replace('\n', '</li>\n')

    # Wrap list items in <ul> tags
    text = text.replace('<li>', '<ul><li>', 1)
    text = text[::-1].replace('</li>', '</ul></li>', 1)[::-1]

    # Add spacing between sections
    text = text.replace('</ul>', '</ul>\n')

    return text

# Configure API key
API_KEY = 'AIzaSyApL1UZAvoJ2ATytTBkPrCkwqcFOrVF4Z8'
genai.configure(api_key=API_KEY)

# Initialize models
model_pro = genai.GenerativeModel('gemini-1.5-pro')
model_flash = genai.GenerativeModel('gemini-1.5-flash')

# Read data from file
def read_data_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def read_history_file(file_path):
    try:
        with open(file_path, 'r') as file:
            history = file.readlines()
    except FileNotFoundError:
        history = []
    return history

def write_history_file(file_path, history):
    with open(file_path, 'w') as file:
        file.writelines(history)

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

data = read_data_file('data.txt')  # Read data from data.txt
history = read_history_file('history.txt')  # Read existing history from history.txt

conversation_start_time = get_current_time()

def generate_response(user_input):
    global history
    user_time = get_current_time()
    history.append(f"User ({user_time}): {user_input}\n")
    prompt = f"Refer to this data while talking to me, but don't refer it unless I ask you to:\n{data}\n\nConversation history:\n" + "".join(history)
    response = model_pro.generate_content(prompt)
    ai_response = to_markdown(response.text)
    ai_time = get_current_time()
    history.append(f"AI ({ai_time}): {ai_response}\n")

    write_history_file('history.txt', history)
    return ai_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    ai_response = generate_response(user_input)
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)