# model.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

def get_model():
    """Get an OpenAI chat model."""
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    return ChatOpenAI(
        model_name="gpt-4o-2024-11-20",
        temperature=0.7
    )

def get_llm():
    """Get the OpenAI language model."""
    return get_model()