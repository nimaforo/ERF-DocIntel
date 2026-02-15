"""
Test enhanced bilingual retrieval with document intelligence.
Tests query translation and comprehensive search across all sources.
"""

import os
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import only what we need - avoid full pipeline imports
from langchain_core.documents import Document
from typing import List, Dict, Any

# Inline minimal DI retriever for testing
class TestDIRetriever:
    """Minimal test version of DocumentIntelligenceRetriever"""
    
    def __init__(self, translation_service=None):
        self.translation_service = translation_service
        self.summaries_dir = Path("outputs/summaries")
        self.chunks_file = Path("outputs/chunks/chunks.json")
        self.extraction_file = Path("outputs/extraction/all_extractions.json")
    
    def retrieve_from_summaries(self, query: str, query_en: str = None, query_fa: str = None) -> List[Document]:
        docs = []
        if not self.summaries_dir.exists():
            return docs
        
        search_queries = [query.lower()]
        if query_en:
            search_queries.append(query_en.lower())
        if query_fa:
            search_queries.append(query_fa.lower())
        
        keywords = set()
        for q in search_queries:
            keywords.update(q.split())
        
        for summary_file in self.summaries_dir.glob("*.md"):
            try:
                with open(summary_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content_lower = content.lower()
                score = sum(1 for kw in keywords if kw in content_lower)
                
                if score > 0:
                    docs.append(Document(
                        page_content=content[:500],  # Preview only
                        metadata={
                            "source": summary_file.name,
                            "type": "summary",
                            "score": score,
                        }
                    ))
            except Exception as e:
                print(f"Warning: Error reading {summary_file}: {e}")
        
        return docs
    
    def retrieve_from_chunks(self, query: str, query_en: str = None, query_fa: str = None) -> List[Document]:
        docs = []
        if not self.chunks_file.exists():
            return docs
        
        search_queries = [query.lower()]
        if query_en:
            search_queries.append(query_en.lower())
        if query_fa:
            search_queries.append(query_fa.lower())
        
        keywords = set()
        for q in search_queries:
            keywords.update(q.split())
        
        try:
            with open(self.chunks_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            for chunk in chunks[:100]:  # Limit for testing
                content = chunk.get('content', chunk.get('text', ''))
                if not content:
                    continue
                
                content_lower = content.lower()
                score = sum(1 for kw in keywords if kw in content_lower)
                
                if score > 0:
                    docs.append(Document(
                        page_content=content[:500],
                        metadata={
                            "source": chunk.get('document', 'Unknown'),
                            "type": "chunk",
                            "score": score,
                        }
                    ))
        except Exception as e:
            print(f"Warning: Error reading chunks: {e}")
        
        return docs
    
    def retrieve_from_extractions(self, query: str, query_en: str = None, query_fa: str = None) -> List[Document]:
        docs = []
        if not self.extraction_file.exists():
            return docs
        
        search_queries = [query.lower()]
        if query_en:
            search_queries.append(query_en.lower())
        if query_fa:
            search_queries.append(query_fa.lower())
        
        keywords = set()
        for q in search_queries:
            keywords.update(q.split())
        
        try:
            with open(self.extraction_file, 'r', encoding='utf-8') as f:
                extractions = json.load(f)
            
            for doc_name, extraction_data in list(extractions.items())[:20]:
                content = json.dumps(extraction_data, ensure_ascii=False)
                content_lower = content.lower()
                
                score = sum(1 for kw in keywords if kw in content_lower)
                
                if score > 0:
                    docs.append(Document(
                        page_content=content[:500],
                        metadata={
                            "source": doc_name,
                            "type": "extraction",
                            "score": score,
                        }
                    ))
        except Exception as e:
            print(f"Warning: Error reading extractions: {e}")
        
        return docs

# Import translation service
try:
    from utils.translation_service import TranslationService
except:
    print("Warning: Could not import TranslationService, using mock")
    class TranslationService:
        def detect_language(self, text):
            if any('\u0600' <= c <= '\u06FF' for c in text):
                return 'fa'
            return 'en'
        
        def translate(self, text, source, target):
            return f"[Translated from {source} to {target}]: {text}"

def test_bilingual_retrieval():
    """Test query translation and retrieval."""
    print("=" * 80)
    print("Testing Enhanced Bilingual Retrieval")
    print("=" * 80)
    
    # Initialize translation service
    translation_service = TranslationService()
    print("✓ Translation service initialized")
    
    # Initialize DI retriever
    di_retriever = TestDIRetriever(translation_service=translation_service)
    print("✓ Document Intelligence retriever initialized")
    
    # Test queries in both languages
    test_queries = [
        "resume requirements",
        "What are the main requirements?",
    ]
    
    for query in test_queries:
        print(f"\n{'=' * 80}")
        print(f"Query: {query}")
        print(f"{'=' * 80}")
        
        # Detect and translate
        lang = translation_service.detect_language(query)
        print(f"Detected language: {lang}")
        
        if lang == 'en':
            query_en = query
            try:
                query_fa = translation_service.translate(query, 'en', 'fa')
                print(f"Translated to FA: {query_fa}")
            except:
                query_fa = None
        else:
            query_fa = query
            try:
                query_en = translation_service.translate(query, 'fa', 'en')
                print(f"Translated to EN: {query_en}")
            except:
                query_en = None
        
        # Retrieve from all sources
        summaries = di_retriever.retrieve_from_summaries(query, query_en, query_fa)
        chunks = di_retriever.retrieve_from_chunks(query, query_en, query_fa)
        extractions = di_retriever.retrieve_from_extractions(query, query_en, query_fa)
        
        # Display results
        print(f"\nSUMMARIES: {len(summaries)} results")
        for i, doc in enumerate(summaries[:2], 1):
            print(f"  [{i}] {doc.metadata.get('source')} - Score: {doc.metadata.get('score')}")
            print(f"      {doc.page_content[:150]}...")
        
        print(f"\nCHUNKS: {len(chunks)} results")
        for i, doc in enumerate(chunks[:2], 1):
            print(f"  [{i}] {doc.metadata.get('source')} - Score: {doc.metadata.get('score')}")
        
        print(f"\nEXTRACTIONS: {len(extractions)} results")
        for i, doc in enumerate(extractions[:2], 1):
            print(f"  [{i}] {doc.metadata.get('source')} - Score: {doc.metadata.get('score')}")
        
        total = len(summaries) + len(chunks) + len(extractions)
        print(f"\n📊 TOTAL: {total} documents from Document Intelligence")

def test_search_functionality():
    """Test individual search functions."""
    print("\n" + "=" * 80)
    print("Testing Individual Search Functions")
    print("=" * 80)
    
    di_retriever = TestDIRetriever()
    
    # Check file locations
    print(f"\n📁 Checking file locations:")
    print(f"   Summaries dir: {di_retriever.summaries_dir}")
    print(f"   Exists: {di_retriever.summaries_dir.exists()}")
    
    if di_retriever.summaries_dir.exists():
        summary_files = list(di_retriever.summaries_dir.glob("*.md"))
        print(f"   Summary files found: {len(summary_files)}")
        for f in summary_files[:5]:
            size = f.stat().st_size / 1024
            print(f"     - {f.name} ({size:.1f} KB)")
    
    print(f"\n   Chunks file: {di_retriever.chunks_file}")
    print(f"   Exists: {di_retriever.chunks_file.exists()}")
    if di_retriever.chunks_file.exists():
        size = di_retriever.chunks_file.stat().st_size / 1024
        print(f"   Size: {size:.1f} KB")
    
    print(f"\n   Extraction file: {di_retriever.extraction_file}")
    print(f"   Exists: {di_retriever.extraction_file.exists()}")
    if di_retriever.extraction_file.exists():
        size = di_retriever.extraction_file.stat().st_size / 1024
        print(f"   Size: {size:.1f} KB")
    
    # Test simple search
    test_query = "resume"
    print(f"\n🔍 Testing search for: '{test_query}'")
    
    summaries = di_retriever.retrieve_from_summaries(test_query)
    print(f"   Summaries: {len(summaries)} results")
    
    chunks = di_retriever.retrieve_from_chunks(test_query)
    print(f"   Chunks: {len(chunks)} results")
    
    extractions = di_retriever.retrieve_from_extractions(test_query)
    print(f"   Extractions: {len(extractions)} results")

def test_translation():
    """Test query translation."""
    print("\n" + "=" * 80)
    print("Testing Query Translation")
    print("=" * 80)
    
    translation_service = TranslationService()
    
    test_cases = [
        "What is this document about?",
        "resume requirements",
        "main points",
    ]
    
    for text in test_cases:
        print(f"\n🔄 Original: {text}")
        try:
            detected = translation_service.detect_language(text)
            print(f"   Detected: {detected}")
            
            if detected == 'en':
                translated = translation_service.translate(text, 'en', 'fa')
                print(f"   Translated to FA: {translated}")
            else:
                translated = translation_service.translate(text, 'fa', 'en')
                print(f"   Translated to EN: {translated}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("\n🚀 Starting Enhanced Retrieval Tests\n")
    
    try:
        # Test translation first
        test_translation()
        
        # Test search functionality
        test_search_functionality()
        
        # Test full bilingual retrieval
        test_bilingual_retrieval()
        
        print("\n" + "=" * 80)
        print("✅ All tests completed!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
