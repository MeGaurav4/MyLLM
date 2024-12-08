"""
Personal LLM Chat Interface
A web application that provides a chat interface for interacting with Google's Gemini AI model.
"""

from typing import List, Optional
import textwrap
from datetime import datetime
from ratelimit import limits, RateLimitException
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, abort
import config

app = Flask(__name__)

def setup_genai() -> None:
    """Initialize the Gemini AI configuration."""
    if not config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=config.GEMINI_API_KEY)

def get_ai_models():
    """Initialize and return AI models."""
    return {
        'pro': genai.GenerativeModel(config.MODEL_PRO),
        'flash': genai.GenerativeModel(config.MODEL_FLASH)
    }

def to_markdown(text: str) -> str:
    """Convert text to HTML-friendly markdown format."""
    text = text.replace('**', '<strong>').replace('__', '<strong>')
    text = text.replace('<strong>', '<strong>').replace('</strong>', '</strong>')
    text = text.replace('<li>', '<ul><li>', 1)
    text = text[::-1].replace('</li>', '</ul></li>', 1)[::-1]
    text = text.replace('</ul>', '</ul>\n')
    return text

def read_file(file_path: str) -> str:
    """Read and return file contents."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        app.logger.error(f"File not found: {file_path}")
        return ""

def read_history() -> List[str]:
    """Read conversation history from file."""
    try:
        with open(config.HISTORY_FILE, 'r') as file:
            history = file.readlines()[-config.MAX_HISTORY_LENGTH:]
        return history
    except FileNotFoundError:
        return []

def write_history(history: List[str]) -> None:
    """Write conversation history to file."""
    try:
        with open(config.HISTORY_FILE, 'w') as file:
            file.writelines(history[-config.MAX_HISTORY_LENGTH:])
    except IOError as e:
        app.logger.error(f"Error writing history: {e}")

def get_current_time() -> str:
    """Return formatted current timestamp."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@limits(calls=config.RATE_LIMIT_CALLS, period=config.RATE_LIMIT_PERIOD)
def generate_response(user_input: str) -> str:
    """Generate AI response for user input with rate limiting."""
    try:
        models = get_ai_models()
        history = read_history()
        data = read_file(config.DATA_FILE)
        
        user_time = get_current_time()
        history.append(f"User ({user_time}): {user_input}\n")
        
        prompt = (
            f"Refer to this data while talking to me, but don't refer it unless I ask you to:\n"
            f"{data}\n\nConversation history:\n" + "".join(history)
        )
        
        response = models['pro'].generate_content(prompt)
        ai_response = to_markdown(response.text)
        
        ai_time = get_current_time()
        history.append(f"AI ({ai_time}): {ai_response}\n")
        write_history(history)
        
        return ai_response
    except RateLimitException:
        return "I'm receiving too many requests right now. Please try again in a moment."
    except Exception as e:
        app.logger.error(f"Error generating response: {e}")
        return "I apologize, but I encountered an error. Please try again."

@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests and return AI responses."""
    user_input = request.form.get('user_input', '').strip()
    
    if not user_input:
        return jsonify({'error': 'Empty input'}), 400
    
    if len(user_input) > config.MAX_INPUT_LENGTH:
        return jsonify({'error': 'Input too long'}), 400
    
    try:
        ai_response = generate_response(user_input)
        return jsonify({'response': ai_response})
    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    setup_genai()
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
