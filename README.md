# Prodoc AI Hospital Tool Chatbot

An intelligent chatbot that can answer questions about the Prodoc AI Hospital Tool by analyzing documentation in real-time using OpenAI's GPT-3.5 model.

## Features

- 📚 Document Analysis: Processes Microsoft Word (.docx) documents containing product documentation
- 🤖 Intelligent Responses: Uses GPT-3.5 to provide context-aware answers
- 📝 Smart Context Management: Automatically handles large documents by prioritizing relevant sections
- 🔍 Token Optimization: Intelligently truncates content while preserving important information
- 📊 Comprehensive Logging: Detailed logging system for monitoring and debugging

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Microsoft Word document containing the Prodoc AI Hospital Tool documentation

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install openai python-docx python-dotenv tiktoken
```

4. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your-api-key-here
```

## Configuration

1. Place your Prodoc AI Hospital Tool documentation file (must be in .docx format) in the project root
2. Ensure the document filename matches the one specified in `main.py` (default: "CEP_Prodoc AI Saas.docx")
3. Add your OpenAI API key to the `.env` file

## Usage

1. Activate the virtual environment if not already activated:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Run the chatbot:
```bash
python main.py
```

3. Start asking questions about the Prodoc AI Hospital Tool
4. Type 'exit', 'quit', or 'bye' to end the conversation

## Logging

The application creates detailed logs with timestamps for each session. Log files are created in the format:
```
prodoc_chatbot_YYYYMMDD_HHMMSS.log
```

Logs include:
- Environment loading status
- Document processing information
- Chat interactions
- Error messages and debugging information

## Error Handling

The chatbot includes robust error handling for:
- Missing or invalid API keys
- Document loading failures
- Token limit management
- API communication issues

## Technical Details

- **Token Management**: Default maximum context size is 12,000 tokens
- **Priority Keywords**: The system prioritizes sections containing key terms like 'introduction', 'overview', 'dashboard', etc.
- **Response Temperature**: Set to 0.7 for balanced creativity and accuracy

## Security Notes

- Never commit your `.env` file or expose your API key
- The `.env` file is automatically ignored by git
- API keys are loaded securely using environment variables

## Troubleshooting

1. **API Key Issues**:
   - Ensure the `.env` file exists in the project root
   - Verify the API key format (no quotes around the key)
   - Check if the API key is valid and not expired

2. **Document Loading Issues**:
   - Verify the document is in .docx format
   - Check if the filename matches exactly
   - Ensure the document is in the project root

3. **Python Environment Issues**:
   - Verify Python version compatibility
   - Ensure all dependencies are installed
   - Check virtual environment activation