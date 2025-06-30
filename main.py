import os
from openai import OpenAI
import dotenv
dotenv.load_dotenv()

# 1) Create a client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def gpt_chatbot(user_input: str) -> str:
    # 2) Call the new method
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",   "content": user_input},
        ],
    )
    # 3) Extract the assistant’s reply
    return response.choices[0].message.content.strip()




if __name__== "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
        response = gpt_chatbot(user_input)
        print("Chatbot: ", response)