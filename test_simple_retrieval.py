"""
Simple test to verify document intelligence outputs exist and can be searched.
"""

import json
from pathlib import Path

def test_file_existence():
    """Check if document intelligence outputs exist."""
    print("=" * 80)
    print("Checking Document Intelligence Output Files")
    print("=" * 80)
    
    # Check summaries
    summaries_dir = Path("outputs/summaries")
    print(f"\n📁 Summaries Directory: {summaries_dir}")
    print(f"   Exists: {summaries_dir.exists()}")
    
    if summaries_dir.exists():
        summary_files = list(summaries_dir.glob("*.md"))
        print(f"   Files found: {len(summary_files)}")
        for f in summary_files:
            size = f.stat().st_size / 1024
            print(f"     ✓ {f.name} ({size:.1f} KB)")
            
            # Read first few lines
            with open(f, 'r', encoding='utf-8') as file:
                lines = file.readlines()[:3]
                print(f"       Preview: {' '.join([l.strip() for l in lines])[:100]}...")
    
    # Check chunks
    chunks_file = Path("outputs/chunks/chunks.json")
    print(f"\n📄 Chunks File: {chunks_file}")
    print(f"   Exists: {chunks_file.exists()}")
    
    if chunks_file.exists():
        size = chunks_file.stat().st_size / 1024
        print(f"   Size: {size:.1f} KB")
        
        with open(chunks_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
            print(f"   Number of chunks: {len(chunks)}")
            if chunks:
                print(f"   First chunk keys: {list(chunks[0].keys())}")
                print(f"   First chunk preview: {chunks[0].get('content', chunks[0].get('text', ''))[:100]}...")
    
    # Check extractions
    extraction_file = Path("outputs/extraction/all_extractions.json")
    print(f"\n📊 Extraction File: {extraction_file}")
    print(f"   Exists: {extraction_file.exists()}")
    
    if extraction_file.exists():
        size = extraction_file.stat().st_size / 1024
        print(f"   Size: {size:.1f} KB")
        
        with open(extraction_file, 'r', encoding='utf-8') as f:
            extractions = json.load(f)
            print(f"   Number of documents: {len(extractions)}")
            if extractions:
                first_doc = list(extractions.keys())[0]
                print(f"   First document: {first_doc}")
                print(f"   First extraction keys: {list(extractions[first_doc].keys())}")

def test_simple_search():
    """Test simple keyword search."""
    print("\n" + "=" * 80)
    print("Testing Simple Keyword Search")
    print("=" * 80)
    
    keywords = ["resume", "requirements", "skill", "experience"]
    
    # Search summaries
    summaries_dir = Path("outputs/summaries")
    if summaries_dir.exists():
        print(f"\n🔍 Searching summaries for keywords: {keywords}")
        
        for summary_file in summaries_dir.glob("*.md"):
            with open(summary_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
                matches = [kw for kw in keywords if kw in content]
                if matches:
                    print(f"   ✓ {summary_file.name}: Found {len(matches)} keywords - {matches}")
    
    # Search chunks
    chunks_file = Path("outputs/chunks/chunks.json")
    if chunks_file.exists():
        print(f"\n🔍 Searching chunks for keywords: {keywords}")
        
        with open(chunks_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
            
            matched_chunks = 0
            for chunk in chunks[:50]:  # First 50 for speed
                content = chunk.get('content', chunk.get('text', '')).lower()
                matches = [kw for kw in keywords if kw in content]
                if matches:
                    matched_chunks += 1
            
            print(f"   ✓ Found {matched_chunks} chunks with keywords (out of {min(50, len(chunks))} checked)")
    
    # Search extractions
    extraction_file = Path("outputs/extraction/all_extractions.json")
    if extraction_file.exists():
        print(f"\n🔍 Searching extractions for keywords: {keywords}")
        
        with open(extraction_file, 'r', encoding='utf-8') as f:
            extractions = json.load(f)
            
            matched_docs = 0
            for doc_name, extraction_data in list(extractions.items())[:20]:
                content = json.dumps(extraction_data, ensure_ascii=False).lower()
                matches = [kw for kw in keywords if kw in content]
                if matches:
                    matched_docs += 1
                    print(f"   ✓ {doc_name}: Found keywords - {matches}")
            
            print(f"   Total: {matched_docs} documents matched (out of {min(20, len(extractions))} checked)")

def test_bilingual_keywords():
    """Test bilingual keyword search."""
    print("\n" + "=" * 80)
    print("Testing Bilingual Keyword Search")
    print("=" * 80)
    
    # Keywords in both English and Farsi
    en_keywords = ["resume", "document", "information"]
    fa_keywords = ["رزومه", "مستند", "اطلاعات"]
    
    summaries_dir = Path("outputs/summaries")
    if summaries_dir.exists():
        print(f"\n🔍 Searching for EN keywords: {en_keywords}")
        print(f"🔍 Searching for FA keywords: {fa_keywords}")
        
        for summary_file in summaries_dir.glob("*.md"):
            with open(summary_file, 'r', encoding='utf-8') as f:
                content = f.read()
                content_lower = content.lower()
                
                en_matches = [kw for kw in en_keywords if kw in content_lower]
                fa_matches = [kw for kw in fa_keywords if kw in content]
                
                if en_matches or fa_matches:
                    print(f"\n   {summary_file.name}:")
                    if en_matches:
                        print(f"     EN: {en_matches}")
                    if fa_matches:
                        print(f"     FA: {fa_matches}")

if __name__ == "__main__":
    print("\n🚀 Starting Simple Retrieval Tests\n")
    
    try:
        # Test file existence
        test_file_existence()
        
        # Test simple search
        test_simple_search()
        
        # Test bilingual
        test_bilingual_keywords()
        
        print("\n" + "=" * 80)
        print("✅ All tests completed!")
        print("=" * 80)
        print("\nNext steps:")
        print("1. These files are now searchable by the enhanced retriever")
        print("2. Queries will be translated to EN and FA")
        print("3. All sources (summaries, chunks, extractions) will be searched")
        print("4. Results will be combined and ranked by relevance")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
