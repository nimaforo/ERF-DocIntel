import sys
import traceback
sys.path.insert(0, '/app')

try:
    from ingestion.processor import DocumentProcessor
    from graph.agent import ConversationalAgent
    
    print("Initializing DocumentProcessor...")
    processor = DocumentProcessor(
        persist_directory='/app/data/chroma_db',
        embedding_model='sentence-transformers/all-MiniLM-L6-v2',
        use_openai_embeddings=False
    )
    print("DocumentProcessor initialized successfully")
    
    print("Initializing ConversationalAgent...")
    agent = ConversationalAgent(
        processor.get_vector_store(),
        llm_provider='ollama'
    )
    print("ConversationalAgent initialized successfully")
    
    print("\nSUCCESS: All components initialized")
    
except Exception as e:
    print(f"\nERROR: {e}")
    traceback.print_exc()
