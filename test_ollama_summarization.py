"""
Test Document Intelligence with Ollama + Qwen2.5
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from document_intelligence.summarization import HierarchicalSummarizer

def test_ollama_summarization():
    """Test summarization with Ollama"""
    print("Testing Ollama Summarization with Qwen2.5...")
    print("=" * 60)
    
    # Create test chunks
    chunks = [
        {
            'chunk_id': '1',
            'content': 'Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. It involves algorithms that can identify patterns and make decisions with minimal human intervention.',
            'type': 'text',
            'section': 'Introduction',
            'content_tokens': 50
        },
        {
            'chunk_id': '2',
            'content': 'یادگیری ماشین یک زیرمجموعه از هوش مصنوعی است که به کامپیوترها اجازه می‌دهد از داده‌ها یاد بگیرند بدون اینکه به صورت صریح برنامه‌ریزی شوند. این شامل الگوریتم‌هایی است که می‌توانند الگوها را شناسایی کنند.',
            'type': 'text',
            'section': 'Persian Text',
            'content_tokens': 50
        }
    ]
    
    try:
        # Initialize with Ollama
        summarizer = HierarchicalSummarizer(
            compression_ratio=0.3,
            use_llm=True,
            llm_provider="ollama",
            model_name="qwen2.5:latest"
        )
        
        print(f"\nInitialized: {summarizer.use_llm}")
        print(f"Provider: {summarizer.llm_provider}")
        print(f"Model: {summarizer.model_name}")
        
        if summarizer.use_llm:
            print("\n✅ LLM initialized successfully!")
            
            # Test summarization
            print("\n" + "-" * 60)
            print("Testing English summarization...")
            summary_en = summarizer._summarize_text(chunks[0]['content'], 'text')
            print(f"Original ({len(chunks[0]['content'])} chars):")
            print(chunks[0]['content'][:100] + "...")
            print(f"\nSummary ({len(summary_en)} chars):")
            print(summary_en)
            
            print("\n" + "-" * 60)
            print("Testing Persian summarization...")
            summarizer.detected_language = 'fa'  # Set to Persian
            summary_fa = summarizer._summarize_text(chunks[1]['content'], 'text')
            print(f"Original ({len(chunks[1]['content'])} chars):")
            print(chunks[1]['content'][:100] + "...")
            print(f"\nSummary ({len(summary_fa)} chars):")
            print(summary_fa)
            
            print("\n" + "=" * 60)
            print("✅ Ollama + Qwen2.5 working correctly!")
            return True
        else:
            print("\n❌ LLM not initialized - check Ollama is running")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ollama_summarization()
    sys.exit(0 if success else 1)
