__module_name__ = "llm"

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_chat_model(temperature: float = 0.7) -> ChatGoogleGenerativeAI:
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found. Check your .env file.")
    try:
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=temperature,
            top_p=0.9,
        )
    except Exception as e:
        raise ValueError(f"Failed to initialize chat model: {str(e)}")
