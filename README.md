# 🏥 Healthcare AI Assistant Chatbot

A sophisticated healthcare chatbot powered by **Groq API** and **Pinecone** vector database, featuring advanced conversation memory, RAG (Retrieval-Augmented Generation), and a modern glass morphism UI design.

## ✨ Features

### 🤖 **AI-Powered Healthcare Assistant**
- **Groq API Integration**: Ultra-fast responses using `llama-3.1-8b-instant` model
- **Medical Knowledge Base**: 5,859+ medical text chunks from comprehensive medical literature
- **RAG System**: Retrieval-Augmented Generation for contextually accurate medical information
- **Smart Context Retrieval**: Automatically finds relevant medical information for each query

### 🧠 **Advanced Memory System**
- **Session-Based Memory**: Each user gets isolated conversation history
- **Context Awareness**: Remembers last 10 exchanges per session
- **Follow-up Intelligence**: Connects dots in your health journey
- **Conversation Continuity**: Seamless multi-turn medical consultations

### 🎨 **Modern UI/UX Design**
- **Glass Morphism**: Beautiful semi-transparent design with backdrop blur effects
- **Gradient Backgrounds**: Seamless green-to-white gradient themes
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern Icons**: FontAwesome 6.5 with floating animations
- **Enhanced Typography**: Inter font family for professional appearance

### 📚 **Medical Text Formatting**
- **Structured Responses**: Proper headings, bullet points, and emphasis
- **Medical Formatting**: Organized treatment options, symptoms, and procedures
- **Easy Reading**: Clear visual hierarchy for complex medical information
- **Professional Layout**: Clinical-grade presentation of medical data

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Groq API Key ([Get it here](https://console.groq.com/))
- Pinecone API Key ([Get it here](https://www.pinecone.io/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/rizwan2004cs/Medibot-chatbot.git
cd healthcare_chatbot_2025
```

2. **Create virtual environment**
```bash
# Using conda (recommended)
conda create -n healthcare-bot python=3.10 -y
conda activate healthcare-bot

# Or using venv
python -m venv healthcare-bot
source healthcare-bot/bin/activate  # Linux/Mac
# healthcare-bot\Scripts\activate   # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
Create a `.env` file in the root directory:
```env
# Healthcare Chatbot API Configuration
GROQ_API_KEY="your_groq_api_key_here"
PINECONE_API_KEY="your_pinecone_api_key_here"
```

5. **Process medical documents and create fresh index**
```bash
python fresh_index.py
```
This will:
- Load and process PDF documents from the `data/` folder
- Create text chunks optimized for medical queries
- Generate embeddings using HuggingFace transformers
- Store everything in a fresh Pinecone index

6. **Start the application**
```bash
python app_with_memory.py
```

7. **Access the chatbot**
Open your browser and navigate to:
```
http://localhost:8080
```

## 🛠️ Technology Stack

### **Backend & AI**
- **Python 3.10+**: Core programming language
- **Flask 3.1.1**: Web framework for API and routing
- **LangChain 0.3.26**: AI framework for LLM orchestration
- **Groq API**: High-performance LLM inference
- **LangChain-Groq**: Groq integration for LangChain

### **Vector Database & Embeddings**
- **Pinecone**: Cloud-native vector database
- **LangChain-Pinecone**: Pinecone integration for vector operations
- **HuggingFace Transformers**: `sentence-transformers/all-MiniLM-L6-v2` for embeddings
- **Sentence Transformers**: Advanced semantic search capabilities

### **Document Processing**
- **PyPDF**: PDF document processing and text extraction
- **LangChain Community**: Document loaders and text splitters
- **Recursive Text Splitter**: Intelligent text chunking for optimal retrieval

### **Frontend & UI**
- **HTML5 & CSS3**: Modern web standards
- **Bootstrap 4.1.3**: Responsive grid system and components
- **FontAwesome 6.5**: Modern icon library
- **Inter Font**: Professional typography
- **Glass Morphism**: Modern UI design principles

## 📁 Project Structure

```
healthcare_chatbot_2025/
├── app_with_memory.py          # Main Flask application with memory
├── fresh_index.py              # Fresh PDF processing and indexing
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── data/
│   └── Medical_book.pdf        # Medical knowledge base
├── src/
│   ├── __init__.py
│   ├── helper.py               # Utility functions for PDF processing
│   └── prompt.py               # System prompts and templates
├── static/
│   └── style.css               # Enhanced UI styling
└── templates/
    └── chat_with_memory.html   # Main chat interface
```

## 🎯 Usage Examples

### **General Medical Queries**
- "What are the symptoms of diabetes?"
- "Tell me about hypertension treatment options"
- "Explain different types of cancer"

### **Follow-up Questions**
- "What medications are commonly prescribed for this?"
- "Are there any side effects I should know about?"
- "What lifestyle changes would help?"

### **Contextual Conversations**
The chatbot remembers your conversation history and can:
- Reference previous questions and answers
- Provide follow-up care recommendations
- Connect related medical topics
- Maintain context across multiple queries

## 🔧 Configuration

### **Memory Settings**
- **Buffer Size**: 10 exchanges (configurable in `app_with_memory.py`)
- **Session Timeout**: Browser session-based
- **Context Window**: Automatic context management

### **RAG Configuration**
- **Chunk Size**: 500 characters with 20-character overlap
- **Retrieval Count**: Top 3 most relevant documents
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Dimensions**: 384

### **API Settings**
- **Model**: `llama-3.1-8b-instant` (Groq)
- **Temperature**: 0.3 (balanced creativity/accuracy)
- **Max Tokens**: 1000 per response

## 🏗️ Development

### **Adding New Medical Documents**
1. Place PDF files in the `data/` directory
2. Run `python fresh_index.py` to reprocess and reindex
3. Restart the application

### **Customizing UI**
- Modify `static/style.css` for styling changes
- Edit `templates/chat_with_memory.html` for layout changes
- Update color schemes in CSS variables

### **Extending Functionality**
- Add new routes in `app_with_memory.py`
- Modify prompts in `src/prompt.py`
- Extend helper functions in `src/helper.py`

## 📊 Performance Metrics

- **Processing Speed**: ~5,859 medical chunks processed
- **Response Time**: Sub-second responses with Groq API
- **Memory Efficiency**: Session-based conversation storage
- **Accuracy**: RAG-enhanced responses with medical literature context

## 🛡️ Security & Privacy

- **API Keys**: Stored securely in environment variables
- **Session Isolation**: Each user gets private conversation memory
- **No Data Persistence**: Conversations are not permanently stored
- **Medical Disclaimer**: Always recommends consulting healthcare professionals


## 🚨 Important Notes

### **Medical Disclaimer**
This chatbot is for informational purposes only and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.

### **API Costs**
- **Groq API**: Generally free tier available with rate limits
- **Pinecone**: Free tier includes 1 index and limited storage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### **Common Issues**

**1. Groq API Key Invalid**
```bash
Error: No GROQ_API_KEY found!
```
- Ensure your Groq API key is correctly set in the `.env` file
- Verify the API key is active on the Groq console

**2. Pinecone Connection Issues**
```bash
Warning: Could not initialize Pinecone
```
- Check your Pinecone API key in the `.env` file
- Ensure your Pinecone account has available indexes

**3. Memory Initialization Warnings**
```bash
LangChainDeprecationWarning: Please see the migration guide
```
- These are deprecation warnings and don't affect functionality
- The app will continue to work normally

**4. PDF Processing Issues**
- Ensure PDF files are in the `data/` directory
- Run `python fresh_index.py` after adding new PDFs
- Check PDF files are not corrupted or password-protected

### **Getting Help**

1. Check the [Issues](https://github.com/rizwan2004cs/Medibot-chatbot/issues) page
2. Review the troubleshooting section above
3. Create a new issue with detailed error information

## 🙏 Acknowledgments

- **Groq**: For providing high-performance LLM inference
- **Pinecone**: For vector database services
- **LangChain**: For the comprehensive AI framework
- **HuggingFace**: For transformer models and embeddings
- **Medical Literature**: For the comprehensive medical knowledge base

## 📞 Support

For support, please:
1. Check the documentation above
2. Search existing [issues](https://github.com/rizwan2004cs/Medibot-chatbot/issues)
3. Create a new issue if needed

---

**Made with ❤️ for healthcare accessibility and AI-powered medical assistance**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.26-orange.svg)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-API-purple.svg)](https://groq.com)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-red.svg)](https://pinecone.io)
