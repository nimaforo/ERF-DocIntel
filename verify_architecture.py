#!/usr/bin/env python3
"""
Quick test script to verify the hexagonal architecture is working.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_container_initialization():
    """Test that the DI container initializes properly."""
    print("Testing Container initialization...")
    try:
        from src.adapters.config import Container
        
        container = Container()
        
        # Test that all adapters can be retrieved
        assert container.get_vector_store() is not None
        assert container.get_llm() is not None
        assert container.get_cache() is not None
        assert container.get_chat_history() is not None
        
        print("✓ Container initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Container initialization failed: {e}")
        return False


def test_models():
    """Test that models are properly defined."""
    print("Testing Models...")
    try:
        from src.shared.models import (
            Document,
            DocumentChunk,
            Query,
            QueryType,
            RetrievalResult,
            AIResponse,
            ChatMessage,
        )
        
        # Create instances
        chunk = DocumentChunk(
            content="Test content",
            source="test.pdf",
        )
        
        query = Query(text="What is this?")
        query.query_type = QueryType.QA
        
        response = AIResponse(content="Test response")
        
        message = ChatMessage(role="user", content="Test message")
        
        print("✓ Models created successfully")
        return True
    except Exception as e:
        print(f"✗ Model creation failed: {e}")
        return False


def test_use_cases():
    """Test that use cases can be instantiated."""
    print("Testing Use Cases...")
    try:
        from src.adapters.config import Container
        
        container = Container()
        
        # Get use cases
        process_query = container.get_process_query_use_case()
        ingest_docs = container.get_ingest_documents_use_case()
        search_docs = container.get_search_documents_use_case()
        summarize = container.get_summarize_documents_use_case()
        extract = container.get_extract_information_use_case()
        
        assert process_query is not None
        assert ingest_docs is not None
        assert search_docs is not None
        assert summarize is not None
        assert extract is not None
        
        print("✓ Use cases created successfully")
        return True
    except Exception as e:
        print(f"✗ Use case creation failed: {e}")
        return False


def test_simple_query(mock=True):
    """Test a simple query with mocks."""
    print("Testing Simple Query (with mocks)...")
    try:
        from src.core.use_cases import ProcessQueryUseCase, ProcessQueryRequest
        from src.core.ports import LLMPort, RetrievalPort, TranslationPort, CachePort, ChatHistoryPort
        from src.shared.models import AIResponse
        
        if not mock:
            # Real test - requires working adapters
            from src.adapters.config import Container
            container = Container()
            use_case = container.get_process_query_use_case()
            request = ProcessQueryRequest(query_text="What is this?")
            response = use_case.execute(request)
            assert response is not None
            print("✓ Real query executed successfully")
            return True
        
        # Mock test
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
        
        use_case = ProcessQueryUseCase(
            llm=MockLLM(),
            retrieval=MockRetrieval(),
            translation=MockTranslation(),
            cache=MockCache(),
            chat_history=MockHistory(),
        )
        
        request = ProcessQueryRequest(query_text="What is this?")
        response = use_case.execute(request)
        
        assert response is not None
        assert response.response.content == "Mock response"
        
        print("✓ Query executed successfully with mocks")
        return True
    except Exception as e:
        print(f"✗ Query execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  HEXAGONAL ARCHITECTURE - SYSTEM VERIFICATION")
    print("=" * 60 + "\n")
    
    results = []
    
    # Run tests
    results.append(("Container", test_container_initialization()))
    results.append(("Models", test_models()))
    results.append(("Use Cases", test_use_cases()))
    results.append(("Query Processing", test_simple_query(mock=True)))
    
    # Print summary
    print("\n" + "=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{name:.<40} {status}")
    
    print("\n" + "=" * 60)
    print(f"Result: {passed}/{total} tests passed")
    print("=" * 60 + "\n")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.\n")
        print("Next steps:")
        print("1. Read IMPLEMENTATION_SUMMARY.md for overview")
        print("2. Run: streamlit run src/adapters/primary/ui/__init__.py")
        print("3. Or run: python main.py")
        print("4. Read HEXAGONAL_ARCHITECTURE.md for detailed guide")
        return True
    else:
        print("❌ Some tests failed. Check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
