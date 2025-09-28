"""
Fresh PDF Processing Script for Healthcare Chatbot
This script processes PDF files from scratch and creates a fresh Pinecone index
"""
from dotenv import load_dotenv
import os
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split, download_hugging_face_embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec 
from langchain_pinecone import PineconeVectorStore

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

print("🚀 Starting Fresh PDF Processing...")
print("=" * 50)

# Step 1: Load PDF files
print("📚 Step 1: Loading PDF files from data/ directory...")
try:
    extracted_data = load_pdf_file(data='data/')
    print(f"✅ Successfully loaded {len(extracted_data)} documents")
    
    # Show some stats about the loaded documents
    total_chars = sum(len(doc.page_content) for doc in extracted_data)
    print(f"📊 Total characters: {total_chars:,}")
    print(f"📄 Average characters per document: {total_chars // len(extracted_data):,}")
except Exception as e:
    print(f"❌ Error loading PDF files: {e}")
    exit(1)

# Step 2: Filter to minimal documents
print("\n🔍 Step 2: Filtering to minimal documents...")
try:
    filter_data = filter_to_minimal_docs(extracted_data)
    print(f"✅ Filtered to {len(filter_data)} clean documents")
except Exception as e:
    print(f"❌ Error filtering documents: {e}")
    exit(1)

# Step 3: Split into text chunks
print("\n✂️ Step 3: Splitting text into chunks...")
try:
    text_chunks = text_split(filter_data)
    print(f"✅ Created {len(text_chunks)} text chunks")
    
    # Show chunk statistics
    chunk_sizes = [len(chunk.page_content) for chunk in text_chunks]
    avg_chunk_size = sum(chunk_sizes) / len(chunk_sizes)
    print(f"📊 Average chunk size: {avg_chunk_size:.0f} characters")
    print(f"📊 Chunk size range: {min(chunk_sizes)} - {max(chunk_sizes)} characters")
except Exception as e:
    print(f"❌ Error splitting text: {e}")
    exit(1)

# Step 4: Initialize embeddings
print("\n🧠 Step 4: Initializing HuggingFace embeddings...")
try:
    embeddings = download_hugging_face_embeddings()
    print("✅ Successfully initialized sentence-transformers/all-MiniLM-L6-v2 embeddings")
    print("📐 Embedding dimension: 384")
except Exception as e:
    print(f"❌ Error initializing embeddings: {e}")
    exit(1)

# Step 5: Connect to Pinecone and manage index
print("\n🌲 Step 5: Managing Pinecone index...")
try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "medical-chatbot"
    
    # Check if index exists and delete it for fresh start
    if pc.has_index(index_name):
        print(f"🗑️ Deleting existing index '{index_name}' for fresh start...")
        pc.delete_index(index_name)
        print("✅ Existing index deleted")
    
    # Create fresh index
    print(f"🆕 Creating fresh index '{index_name}'...")
    pc.create_index(
        name=index_name,
        dimension=384,  # sentence-transformers/all-MiniLM-L6-v2 dimension
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    print("✅ Fresh index created successfully")
    
except Exception as e:
    print(f"❌ Error managing Pinecone index: {e}")
    exit(1)

# Step 6: Create and populate vector store
print("\n📥 Step 6: Creating vector store and uploading embeddings...")
try:
    print("⏳ This may take a few minutes to process all chunks...")
    
    docsearch = PineconeVectorStore.from_documents(
        documents=text_chunks,
        index_name=index_name,
        embedding=embeddings, 
    )
    
    print("✅ Vector store created successfully!")
    print(f"📊 Uploaded {len(text_chunks)} document chunks to Pinecone")
    
except Exception as e:
    print(f"❌ Error creating vector store: {e}")
    exit(1)

# Step 7: Test the vector store
print("\n🧪 Step 7: Testing vector store with sample query...")
try:
    test_query = "What are the symptoms of diabetes?"
    results = docsearch.similarity_search(test_query, k=3)
    
    print(f"✅ Test query successful!")
    print(f"📝 Query: '{test_query}'")
    print(f"📊 Retrieved {len(results)} relevant documents")
    
    for i, result in enumerate(results, 1):
        preview = result.page_content[:100].replace('\n', ' ')
        print(f"  {i}. {preview}...")
        
except Exception as e:
    print(f"❌ Error testing vector store: {e}")
    exit(1)

print("\n" + "=" * 50)
print("🎉 FRESH PDF PROCESSING COMPLETED SUCCESSFULLY!")
print("=" * 50)
print("📋 Summary:")
print(f"   • Processed: {len(extracted_data)} PDF pages")
print(f"   • Created: {len(text_chunks)} text chunks")
print(f"   • Index: '{index_name}' (fresh)")
print(f"   • Embeddings: 384-dimensional vectors")
print(f"   • Ready for: Healthcare chatbot with Groq API")
print("\n🚀 You can now start the chatbot application!")