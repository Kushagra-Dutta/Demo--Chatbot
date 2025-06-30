import os
from openai import OpenAI
import dotenv
from docx import Document
import tiktoken
import logging
from datetime import datetime
import sys

# Configure logging
log_filename = f"prodoc_chatbot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()
logger.info("Environment variables loaded")
api_key = os.getenv("OPENAI_API_KEY")
# Create a client
try:
    client = OpenAI(
        api_key=api_key,
    )
    logger.info(f"OpenAI client initialized successfully : {api_key}")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    raise

def read_docx_file(file_path):
    """
    Read content from a .docx file and return as text
    """
    try:
        logger.info(f"Attempting to read document: {file_path}")
        doc = Document(file_path)
        full_text = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # Only add non-empty paragraphs
                full_text.append(paragraph.text)
        
        result = '\n'.join(full_text)
        logger.info(f"Successfully read document with {len(full_text)} paragraphs")
        return result
    except Exception as e:
        logger.error(f"Error reading docx file: {e}")
        return None

def count_tokens(text, model="gpt-3.5-turbo"):
    """
    Count the number of tokens in a text string
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        # Fallback estimation: roughly 4 characters per token
        return len(text) // 4

def truncate_text_to_fit_context(text, max_tokens=3000):
    """
    Truncate text to fit within token limits while preserving important sections
    """
    if count_tokens(text) <= max_tokens:
        return text
    
    # Split into sections and prioritize key information
    sections = text.split('\n\n')
    
    # Keep the introduction and key sections
    important_keywords = [
        'introduction', 'overview', 'dashboard', 'conversations', 
        'leads', 'appointments', 'settings', 'features'
    ]
    
    priority_sections = []
    other_sections = []
    
    for section in sections:
        if any(keyword in section.lower() for keyword in important_keywords):
            priority_sections.append(section)
        else:
            other_sections.append(section)
    
    # Start with priority sections
    result_text = '\n\n'.join(priority_sections)
    current_tokens = count_tokens(result_text)
    
    # Add other sections until we hit the limit
    for section in other_sections:
        section_tokens = count_tokens(section)
        if current_tokens + section_tokens <= max_tokens:
            result_text += '\n\n' + section
            current_tokens += section_tokens
        else:
            break
    
    return result_text

def gpt_chatbot_with_document(user_input: str, document_content: str) -> str:
    """
    Chat with GPT using document content as context
    """
    logger.info("Processing new chat request")
    
    # Truncate document content to fit within context window
    truncated_content = truncate_text_to_fit_context(document_content, max_tokens=3000)
    logger.debug(f"Document content truncated to {count_tokens(truncated_content)} tokens")
    
    # Create system message with document context
    system_message = f"""You are a helpful assistant that answers questions based on the provided document about Prodoc AI Hospital Tool. 

Here is the document content for reference:

{truncated_content}

Please answer questions based only on the information provided in this document. If the information is not in the document, please say so. Be specific and helpful in your responses."""

    try:
        logger.debug(f"Sending request to OpenAI API with user input: {user_input[:100]}...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input},
            ],
            max_tokens=1000,
            temperature=0.7
        )
        logger.info("Successfully received response from OpenAI API")
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error in chat completion: {e}")
        return f"Sorry, I encountered an error: {e}"

def main():
    logger.info("Starting Prodoc AI Chatbot")
    
    # Load the document content
    docx_file_path = "CEP_Prodoc AI Saas.docx"
    
    print("Loading document...")
    document_content = read_docx_file(docx_file_path)
    
    if not document_content:
        logger.error("Failed to load document")
        print("Failed to load document. Please check the file path.")
        return
    
    token_count = count_tokens(document_content)
    logger.info(f"Document loaded successfully with {token_count} tokens")
    print(f"Document loaded successfully! ({token_count} tokens)")
    print("You can now ask questions about the Prodoc AI Hospital Tool.")
    print("Type 'exit', 'quit', or 'bye' to end the conversation.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            logger.info("User requested to end conversation")
            print("Goodbye!")
            break
        
        if not user_input.strip():
            continue
            
        print("Thinking...")
        logger.info(f"Processing user input: {user_input[:100]}...")
        response = gpt_chatbot_with_document(user_input, document_content)
        logger.info("Response generated successfully")
        print(f"Chatbot: {response}\n")

if __name__ == "__main__":
    main()