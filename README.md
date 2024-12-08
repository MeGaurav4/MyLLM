# Personal LLM Chat Interface

A sleek web interface for interacting with Google's Gemini AI model that can be trained on your personal data. This application provides a modern chat interface that allows users to have conversations with the Gemini AI model while maintaining conversation history and referring to your personal knowledge base.

## Features

- Modern, responsive chat interface
- Real-time AI responses using Gemini Pro model
- Personal knowledge base integration
- Conversation history tracking
- Markdown support for AI responses
- Dark mode UI

## Setup

1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   Copy the `.env.example` file to `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. Set up your personal data:
   - Copy `data.txt.example` to `data.txt`
   - Edit `data.txt` with your personal information
   - The `history.txt` file will be automatically created when you start chatting

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
my_llm/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── templates/          # HTML templates
│   └── index.html     # Main chat interface
├── data.txt           # Your personal knowledge base (not in git)
├── data.txt.example   # Example knowledge base template
├── history.txt        # Conversation history (not in git)
├── history.txt.example # Example history template
└── requirements.txt   # Project dependencies
```

## Personal Data Files

### data.txt
This file contains your personal information that the AI will use to answer questions. Create this file based on `data.txt.example` and add your own information. This file is not tracked by git to protect your privacy.

### history.txt
This file stores your conversation history with the AI. It's automatically created and updated as you chat. This file is not tracked by git to protect your privacy.

## Security

- API keys are stored in environment variables
- Personal data files are excluded from git
- Input validation implemented
- Rate limiting for API calls

## License

MIT License
