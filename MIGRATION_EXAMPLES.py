"""
Migration Helper Script

This script helps demonstrate how to migrate from the old architecture to the new hexagonal architecture.
"""

from pathlib import Path
from typing import List

# Example: How to use the new architecture

def example_process_query():
    """Example: Process a user query using the new architecture."""
    from src.adapters.config import Container
    from src.core.use_cases import ProcessQueryRequest
    
    # Initialize container (automatically wires all dependencies)
    config = {
        "use_ollama": True,  # Use local Ollama
        "ollama_model": "qwen2.5:latest",
    }
    container = Container(config)
    
    # Get the use case
    use_case = container.get_process_query_use_case()
    
    # Create request
    request = ProcessQueryRequest(
        query_text="What are the main benefits of hexagonal architecture?",
        user_id="user123",
        session_id="session456",
    )
    
    # Execute
    response = use_case.execute(request)
    
    # Print results
    print(f"Query: {response.query}")
    print(f"Type: {response.query_type}")
    print(f"Response: {response.response.content}")
    print(f"Processing time: {response.processing_time:.2f}s")
    print(f"Sources: {len(response.source_documents)}")


def example_ingest_documents():
    """Example: Ingest documents using the new architecture."""
    from src.adapters.config import Container
    from src.shared.models import DocumentChunk
    
    container = Container()
    
    # Load documents
    loader = container.get_document_loader()
    documents = loader.load_documents("./data/raw")
    
    # Process documents
    processor = container.get_document_processor()
    chunks = []
    for doc in documents:
        processed_doc = processor.process_document(doc)
        chunks.extend(processed_doc.chunks)
    
    # Ingest into vector store
    ingest_use_case = container.get_ingest_documents_use_case()
    result = ingest_use_case.execute(chunks)
    
    print(f"Ingested {result['documents_ingested']} chunks")


def example_search_documents():
    """Example: Search documents using the new architecture."""
    from src.adapters.config import Container
    
    container = Container()
    
    # Get search use case
    search_use_case = container.get_search_documents_use_case()
    
    # Search
    result = search_use_case.execute("hexagonal architecture", k=5)
    
    print(f"Found {result.total_results} results")
    for i, doc in enumerate(result.documents, 1):
        print(f"{i}. {doc.source}")
        print(f"   {doc.content[:100]}...")


def example_custom_configuration():
    """Example: Use custom configuration."""
    from src.adapters.config import Container
    
    config = {
        "use_ollama": False,  # Use OpenAI
        "openai_model": "gpt-4-turbo-preview",
        "chunk_size": 2000,
        "use_file_cache": True,
        "use_file_history": True,
        "openai_api_key": "your-key-here",
    }
    
    container = Container(config)
    
    # Now all services use the configuration
    use_case = container.get_process_query_use_case()


def example_testing():
    """Example: Testing with mocked adapters."""
    from src.core.use_cases import ProcessQueryUseCase
    from src.core.ports import LLMPort, RetrievalPort, TranslationPort, CachePort, ChatHistoryPort
    from src.shared.models import AIResponse
    
    # Create mocks
    class MockLLM(LLMPort):
        def generate_response(self, prompt, context=None, temperature=0.7, max_tokens=1000):
            return AIResponse(content="Mock response")
        def classify_query(self, query):
            return "qa"
        def summarize(self, text, max_length=500):
            return "Mock summary"
        def extract_information(self, text, extraction_type):
            return {"result": "Mock extraction"}
    
    class MockRetrieval(RetrievalPort):
        def retrieve(self, query, k=5):
            return []
    
    class MockTranslation(TranslationPort):
        def translate(self, text, source_lang, target_lang):
            return text
        def detect_language(self, text):
            return "en"
    
    class MockCache(CachePort):
        def get(self, key):
            return None
        def set(self, key, value, ttl=None):
            pass
        def delete(self, key):
            pass
        def clear(self):
            pass
    
    class MockHistory(ChatHistoryPort):
        def save_conversation(self, session_id, messages):
            pass
        def load_conversation(self, session_id):
            return []
        def append_message(self, session_id, message):
            pass
        def delete_conversation(self, session_id):
            pass
    
    # Create use case with mocks
    use_case = ProcessQueryUseCase(
        llm=MockLLM(),
        retrieval=MockRetrieval(),
        translation=MockTranslation(),
        cache=MockCache(),
        chat_history=MockHistory(),
    )
    
    # Test
    from src.core.use_cases import ProcessQueryRequest
    request = ProcessQueryRequest(query_text="Test query")
    response = use_case.execute(request)
    
    assert response.response.content == "Mock response"
    print("✓ Test passed!")


if __name__ == "__main__":
    print("Migration Examples")
    print("=" * 50)
    
    print("\n1. Processing a query...")
    example_process_query()
    
    print("\n2. Ingesting documents...")
    example_ingest_documents()
    
    print("\n3. Searching documents...")
    example_search_documents()
    
    print("\n4. Custom configuration...")
    example_custom_configuration()
    
    print("\n5. Testing with mocks...")
    example_testing()
