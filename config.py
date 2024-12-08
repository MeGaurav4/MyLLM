"""Configuration settings for the LLM Chat application."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MODEL_PRO = 'gemini-1.5-pro'
MODEL_FLASH = 'gemini-1.5-flash'

# File Paths
DATA_FILE = 'data.txt'
HISTORY_FILE = 'history.txt'

# Rate Limiting
RATE_LIMIT_CALLS = 60  # Number of calls
RATE_LIMIT_PERIOD = 60  # Time period in seconds

# Flask Configuration
DEBUG = False
HOST = '0.0.0.0'
PORT = 5000

# Chat Configuration
MAX_HISTORY_LENGTH = 100  # Maximum number of messages to keep in history
MAX_INPUT_LENGTH = 1000   # Maximum length of user input
