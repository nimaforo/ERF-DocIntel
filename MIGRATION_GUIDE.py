"""
Quick Start Guide for Hexagonal Architecture

This guide will help you get started with the new architecture.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def quick_start_guide():
    """Print quick start guide."""
    guide = """
HEXAGONAL ARCHITECTURE - QUICK START GUIDE

1. UNDERSTAND THE STRUCTURE
   ├── src/core/              → Pure business logic (framework-independent)
   ├── src/adapters/          → Technology implementations (frameworks)
   ├── src/shared/            → Common models and exceptions
   └── src/infrastructure/    → Technical utilities

2. KEY COMPONENTS

   PORTS (Interfaces):
   - LLMPort: Generate responses, classify queries
   - VectorStorePort: Store and retrieve documents
   - TranslationPort: Translate text between languages
   - CachePort: Cache query results
   - ChatHistoryPort: Store conversation history

   ADAPTERS (Implementations):
   - OpenAILLMAdapter, OllamaLLMAdapter: LLM implementations
   - ChromaVectorStoreAdapter: Vector store implementation
   - DocumentLoaderAdapter, DocumentProcessorAdapter: Document handling
   - InMemoryCacheAdapter, FileCacheAdapter: Caching strategies
   - FileChatHistoryAdapter: Conversation storage

   DOMAIN SERVICES (Business Logic):
   - QueryClassifier: Classify query types
   - DocumentRetriever: Retrieve relevant documents
   - ResponseGenerator: Generate AI responses
   - DocumentTranslator: Translate content
   - ConversationManager: Manage chat

   USE CASES (Workflows):
   - ProcessQueryUseCase: End-to-end query processing
   - IngestDocumentsUseCase: Ingest documents into vector store
   - SearchDocumentsUseCase: Search documents
   - SummarizeDocumentsUseCase: Summarize text
   - ExtractInformationUseCase: Extract structured info

3. RUNNING THE APPLICATION

   Option A: Streamlit UI
   $ streamlit run src/adapters/primary/ui/__init__.py

   Option B: Main entry point
   $ python main.py

4. BASIC USAGE EXAMPLE

   from src.adapters.config import Container
   from src.core.use_cases import ProcessQueryRequest

   # Initialize
   container = Container()

   # Get use case
   use_case = container.get_process_query_use_case()

   # Create request
   request = ProcessQueryRequest(query_text="Your question here")

   # Execute
   response = use_case.execute(request)

   # Use response
   print(response.response.content)

5. CHANGING IMPLEMENTATIONS

   # Use OpenAI instead of Ollama
   config = {"use_ollama": False}
   container = Container(config)

   # Use file cache instead of in-memory
   config = {"use_file_cache": True}
   container = Container(config)

6. TESTING

   Create mocks that implement ports and inject them:

   class MockLLM(LLMPort):
       def generate_response(self, ...):
           return AIResponse(content="Mock")

   use_case = ProcessQueryUseCase(llm=MockLLM(), ...)
   response = use_case.execute(request)

7. ADDING NEW FEATURES

   a) Create a port (interface) for new service
   b) Implement adapter(s) for that port
   c) Add to Container for dependency injection
   d) Use in domain services or use cases
   e) Can be swapped without changing core logic

8. BENEFITS OF THIS ARCHITECTURE

   ✓ Testable: No framework dependencies in core
   ✓ Flexible: Swap implementations easily
   ✓ Maintainable: Clear separation of concerns
   ✓ Scalable: Add new adapters without touching core
   ✓ Framework-agnostic: Could use Flask, FastAPI, etc.

9. ENVIRONMENT VARIABLES

   USE_LOCAL_MODEL=true              # Use Ollama (default)
   LOCAL_MODEL_NAME=qwen2.5:latest   # Model to use
   OPENAI_API_KEY=...                # For OpenAI
   OPENAI_MODEL=gpt-4-turbo-preview  # Model

10. CONFIGURATION OPTIONS

    use_ollama=True                   # Use local or OpenAI
    ollama_model="qwen2.5:latest"     # Model name
    openai_model="gpt-4-turbo-preview"
    chunk_size=1000                   # Document chunk size
    use_file_cache=False              # In-memory cache
    use_file_history=True             # File-based history
    chroma_db_path="./data/chroma_db"
"""
    print(guide)


def example_process_query():
    """Show example of processing a query."""
    from src.adapters.config import Container
    from src.core.use_cases import ProcessQueryRequest
    
    print_header("Example: Process a Query")
    
    print("Code:")
    print("""
from src.adapters.config import Container
from src.core.use_cases import ProcessQueryRequest

# Initialize container (DI)
container = Container()

# Get use case
use_case = container.get_process_query_use_case()

# Create request
request = ProcessQueryRequest(
    query_text="What is hexagonal architecture?",
    user_id="user123",
    session_id="session456",
)

# Execute
response = use_case.execute(request)

# Use results
print(f"Query Type: {response.query_type}")
print(f"Response: {response.response.content}")
print(f"Sources: {len(response.source_documents)}")
print(f"Time: {response.processing_time:.2f}s")
    """)
    
    print("\nExecution:")
    try:
        container = Container()
        use_case = container.get_process_query_use_case()
        request = ProcessQueryRequest(
            query_text="What is the hexagonal architecture?",
        )
        response = use_case.execute(request)
        print(f"✓ Query processed successfully")
        print(f"  Query Type: {response.query_type}")
        print(f"  Response Length: {len(response.response.content)} chars")
        print(f"  Processing Time: {response.processing_time:.2f}s")
    except Exception as e:
        print(f"✗ Error: {e}")


def example_change_config():
    """Show example of changing configuration."""
    print_header("Example: Change Configuration")
    
    print("Code:")
    print("""
config = {
    "use_ollama": False,  # Use OpenAI instead
    "openai_model": "gpt-4-turbo-preview",
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
}
container = Container(config)

# All use cases now use OpenAI
use_case = container.get_process_query_use_case()
response = use_case.execute(request)
    """)
    
    print("Result: All services now use the new configuration!")


def example_testing():
    """Show example of testing."""
    print_header("Example: Testing with Mocks")
    
    print("Code:")
    print("""
class MockLLM(LLMPort):
    def generate_response(self, prompt, ...):
        return AIResponse(content="Mock response")

class MockRetrieval(RetrievalPort):
    def retrieve(self, query, k=5):
        return []

# Inject mocks
use_case = ProcessQueryUseCase(
    llm=MockLLM(),
    retrieval=MockRetrieval(),
    translation=MockTranslation(),
    cache=MockCache(),
    chat_history=MockHistory(),
)

# Test
request = ProcessQueryRequest(query_text="Test")
response = use_case.execute(request)
assert response.response.content == "Mock response"
    """)
    
    print("Result: Services are decoupled and mockable!")


def directory_tree():
    """Print directory tree."""
    print_header("Project Structure")
    
    tree = """
tamrin2/
├── src/                           # New hexagonal architecture
│   ├── core/                      # DOMAIN LOGIC (INDEPENDENT)
│   │   ├── domain/                # Domain services
│   │   ├── ports/                 # Port interfaces
│   │   └── use_cases/             # Use cases (orchestrators)
│   │
│   ├── adapters/                  # IMPLEMENTATIONS (FRAMEWORK DEPENDENT)
│   │   ├── primary/               # Inbound adapters (UI, API)
│   │   │   └── ui/                # Streamlit adapter
│   │   ├── secondary/             # Outbound adapters (services)
│   │   │   ├── document_processing/
│   │   │   ├── vector_store/
│   │   │   ├── llm/
│   │   │   ├── translation/
│   │   │   ├── cache/
│   │   │   └── history/
│   │   └── config/                # DI Container
│   │
│   ├── infrastructure/            # Technical utilities
│   │   └── logging/
│   │
│   └── shared/                    # Common code
│       ├── models/                # Value objects
│       └── exceptions/            # Custom exceptions
│
├── app/                           # OLD ARCHITECTURE (KEEP FOR REFERENCE)
├── graph/
├── ingestion/
├── utils/
├── document_intelligence/
│
├── main.py                        # New entry point
├── HEXAGONAL_ARCHITECTURE.md      # Architecture documentation
├── MIGRATION_EXAMPLES.py          # Migration examples
└── MIGRATION_GUIDE.py             # This file
"""
    print(tree)


def main():
    """Main entry point."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  HEXAGONAL ARCHITECTURE - QUICK START GUIDE".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Print structure
    directory_tree()
    
    # Print guide
    quick_start_guide()
    
    # Print examples
    example_process_query()
    example_change_config()
    example_testing()
    
    print_header("Next Steps")
    print("""
1. Read HEXAGONAL_ARCHITECTURE.md for detailed documentation
2. Review MIGRATION_EXAMPLES.py for more code examples
3. Start with: python main.py  (or streamlit run ...)
4. Check src/adapters/primary/ui/__init__.py for UI implementation
5. Explore src/core/use_cases/__init__.py to understand workflows

Happy coding! 🎉
    """)


if __name__ == "__main__":
    main()
