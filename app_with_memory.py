from flask import Flask, render_template, jsonify, request, session
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain_pinecone import PineconeVectorStore
from src.helper import download_hugging_face_embeddings
from dotenv import load_dotenv
from src.prompt import system_prompt
import os
import uuid

app = Flask(__name__)
app.secret_key = "healthcare_chatbot_secret_key"  # Required for sessions

load_dotenv()

# Initialize Groq API
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

if GROQ_API_KEY:
    print("Using Groq API")
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY
    chatModel = ChatGroq(
        model="llama-3.1-8b-instant",  # Current available model
        temperature=0.3,
        max_tokens=1000
    )
    api_provider = "Groq"
else:
    print("No GROQ_API_KEY found! Please add GROQ_API_KEY to .env file")
    chatModel = None
    api_provider = "None"

# Initialize Pinecone for RAG
vectorstore = None
if PINECONE_API_KEY:
    try:
        print("Initializing Pinecone vector store...")
        os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
        embeddings = download_hugging_face_embeddings()
        vectorstore = PineconeVectorStore(
            index_name="medical-chatbot",
            embedding=embeddings
        )
        print("✅ Pinecone vector store initialized successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize Pinecone: {e}")
        vectorstore = None
else:
    print("⚠️ No PINECONE_API_KEY found - running without RAG capabilities")

# Enhanced prompt with conversation context and RAG
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful medical assistant AI. You provide general medical information based on medical knowledge and always advise users to consult with healthcare professionals for specific medical advice.

Context from medical documents:
{context}

Key guidelines:
- Use the provided medical context to give accurate information
- Remember the conversation context and refer to previous messages when relevant
- If a user asks follow-up questions, connect them to what was discussed earlier
- Be empathetic and understanding
- Always recommend consulting healthcare professionals for diagnosis and treatment
- Provide clear, accurate, and helpful information with proper formatting"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Dictionary to store memory for each session
session_memories = {}

def get_memory_for_session(session_id):
    """Get or create memory for a specific session"""
    if session_id not in session_memories:
        session_memories[session_id] = ConversationBufferWindowMemory(
            k=10,  # Remember last 10 exchanges
            return_messages=True,
            memory_key="chat_history"
        )
    return session_memories[session_id]

@app.route("/")
def index():
    # Create a new session ID if it doesn't exist
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('chat_with_memory.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    if not chatModel:
        return "No AI API configured. Please add GROQ_API_KEY to your .env file."
    
    # Get session ID
    session_id = session.get('session_id', str(uuid.uuid4()))
    if 'session_id' not in session:
        session['session_id'] = session_id
    
    msg = request.form["msg"]
    input_text = msg
    print(f"Session {session_id[:8]}... - User input: {input_text}")
    print(f"Using {api_provider} API")
    
    try:
        # Get memory for this session
        memory = get_memory_for_session(session_id)
        
        # Get conversation history
        chat_history = memory.chat_memory.messages
        
        # Get relevant context from Pinecone if available
        context = ""
        if vectorstore:
            try:
                docs = vectorstore.similarity_search(msg, k=3)
                context = "\n\n".join([doc.page_content for doc in docs])
                print(f"✅ Retrieved {len(docs)} relevant documents from Pinecone")
            except Exception as e:
                print(f"⚠️ Warning: Could not retrieve from Pinecone: {e}")
                context = "No specific medical context available."
        else:
            context = "No specific medical context available."
        
        # Format the prompt with conversation history and context
        formatted_prompt = prompt.format_messages(
            chat_history=chat_history,
            context=context,
            input=msg
        )
        
        # Get response from the AI
        response = chatModel.invoke(formatted_prompt)
        answer = response.content
        
        # Save the conversation to memory
        memory.chat_memory.add_user_message(msg)
        memory.chat_memory.add_ai_message(answer)
        
        print(f"Response: {answer}")
        print(f"Conversation history length: {len(chat_history) + 2}")  # +2 for the new messages
        
        return str(answer)
        
    except Exception as e:
        print(f"Error: {e}")
        if "insufficient_quota" in str(e) or "429" in str(e):
            return f"{api_provider} API quota exceeded. Please check your billing and usage."
        elif "rate_limit" in str(e).lower():
            return f"{api_provider} API rate limit exceeded. Please wait a moment and try again."
        elif "api_key" in str(e).lower() or "authentication" in str(e).lower():
            return f"{api_provider} API key is invalid. Please check your API key configuration."
        else:
            return f"Error with {api_provider}: {str(e)}"

@app.route("/clear", methods=["POST"])
def clear_conversation():
    """Clear the conversation history for the current session"""
    session_id = session.get('session_id')
    if session_id and session_id in session_memories:
        del session_memories[session_id]
        print(f"Cleared conversation history for session {session_id[:8]}...")
    return jsonify({"status": "cleared"})

@app.route("/history", methods=["GET"])
def get_history():
    """Get the conversation history for the current session"""
    session_id = session.get('session_id')
    if session_id and session_id in session_memories:
        memory = session_memories[session_id]
        messages = []
        for msg in memory.chat_memory.messages:
            if isinstance(msg, HumanMessage):
                messages.append({"type": "human", "content": msg.content})
            elif isinstance(msg, AIMessage):
                messages.append({"type": "ai", "content": msg.content})
        return jsonify({"history": messages})
    return jsonify({"history": []})

if __name__ == '__main__':
    print(f"Starting Healthcare Chatbot with {api_provider} API")
    print("Features:")
    print("- ✅ Conversation Memory (remembers context)")
    print("- ✅ Session-based conversations")
    print("- ✅ Medical assistance with context awareness")
    app.run(host="0.0.0.0", port=8080, debug=True)