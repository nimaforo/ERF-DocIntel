"""
Test script for Part 2: Semantic Chunking System
"""

import json
from pathlib import Path
from document_intelligence.pipeline import DocumentIntelligencePipeline


def main():
    """Test Part 2 chunking on processed documents."""
    
    print("="*70)
    print("TESTING PART 2: SEMANTIC CHUNKING SYSTEM")
    print("="*70)
    
    # Find processed documents
    processed_file = Path("outputs/processed_documents.json")
    
    if not processed_file.exists():
        print("\n❌ Error: No processed documents found!")
        print("   Run test_part1.py first to process documents.")
        return
    
    # Load processed documents
    with open(processed_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract documents list
    processed_docs = data.get('documents', [])
    
    if not processed_docs:
        print("\n❌ Error: No documents found in processed file!")
        return
    
    print(f"\n📄 Found {len(processed_docs)} processed documents")
    
    # Initialize pipeline
    pipeline = DocumentIntelligencePipeline()
    
    # Run Part 2 chunking
    chunks = pipeline.run_part2_chunking(processed_docs)
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    
    print(f"\n📊 Total Chunks Created: {len(chunks)}")
    
    # Chunk type statistics
    chunk_types = {}
    total_tokens = 0
    for chunk in chunks:
        chunk_type = chunk['type']
        chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
        total_tokens += chunk['content_tokens']
    
    print("\n📋 Chunk Types:")
    for chunk_type, count in sorted(chunk_types.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(chunks) * 100) if chunks else 0
        print(f"   {chunk_type}: {count} ({percentage:.1f}%)")
    
    avg_tokens = total_tokens / len(chunks) if chunks else 0
    print(f"\n🔢 Token Statistics:")
    print(f"   Total tokens: {total_tokens:,}")
    print(f"   Average tokens/chunk: {avg_tokens:.1f}")
    
    # Show sample chunks
    print("\n📝 Sample Chunks:")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n   Chunk {chunk['chunk_id']} ({chunk['type']}):")
        print(f"     Section: {chunk['section']}")
        print(f"     Tokens: {chunk['content_tokens']}")
        print(f"     Summary: {chunk['chunk_summary'][:80]}...")
    
    # Output files
    print("\n📁 Output Files Generated:")
    chunks_file = Path("outputs/chunks/chunks.json")
    report_file = Path("outputs/reports/chunking_report.md")
    
    if chunks_file.exists():
        print(f"   ✓ {chunks_file}")
    if report_file.exists():
        print(f"   ✓ {report_file}")
    
    print("\n" + "="*70)
    print("✅ PART 2 TEST COMPLETED SUCCESSFULLY")
    print("="*70)
    print("\nNext step: Run Part 3 (Multi-Technique Prompting)")
    print("Or view the chunking report:")
    print(f"  cat outputs/reports/chunking_report.md")


if __name__ == "__main__":
    main()
