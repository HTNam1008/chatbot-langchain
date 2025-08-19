# chatbot.py
from typing import List, Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from model import get_llm

def create_chatbot():
    """Create a chatbot using OpenAI."""
    # Get the language model
    llm = get_llm()
    
    # System prompt for the AI assistant
    system_prompt = """
    You are a helpful and friendly AI assistant designed to respond only to queries related to Artificial Intelligence. 
    You must not ask the user any questions-simply respond concisely, clearly, and directly to their query using short, relevant answers. 
    Use bullet points only when it improves clarity. Politely acknowledge greetings or thanks with brief responses. 
    If the query is unrelated to AI, respond with: 'I am here to assist with AI-related topics. Could you please ask a question related to that?'
    """
    
    # Create a prompt template
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])
    
    # Create a simple chain
    chain = prompt | llm
    
    return chain

def get_response(chain, user_input: str, chat_history: List[Dict[str, Any]] = None) -> str:
    """Get a response from the chatbot for the given user input."""
    try:
        # Convert Streamlit message format to LangChain message format
        langchain_messages = []
        if chat_history:
            for msg in chat_history[:-1]:  # Exclude the most recent user message as we'll add it separately
                if msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    langchain_messages.append(AIMessage(content=msg["content"]))
        
        # Invoke the chain with properly formatted history and question
        response = chain.invoke({
            "chat_history": langchain_messages,
            "question": user_input
        })
        
        # Return the content of the response
        if hasattr(response, "content"):
            return response.content
        return str(response)
        
    except Exception as e:
        return f"I encountered an error: {str(e)}. Please try again."