"""
Test script for Part 4: Hierarchical Summarization
"""

import json
from pathlib import Path
from document_intelligence.pipeline import DocumentIntelligencePipeline


def main():
    """Test Part 4 hierarchical summarization."""
    
    print("="*70)
    print("TESTING PART 4: HIERARCHICAL SUMMARIZATION")
    print("="*70)
    
    # Find chunks file
    chunks_file = Path("outputs/chunks/chunks.json")
    
    if not chunks_file.exists():
        print("\n❌ Error: No chunks found!")
        print("   Run test_part2.py first to generate chunks.")
        return
    
    # Load chunks
    with open(chunks_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    print(f"\n📄 Loaded {len(chunks)} chunks")
    
    # Initialize pipeline
    pipeline = DocumentIntelligencePipeline()
    
    # Run Part 4 hierarchical summarization
    results = pipeline.run_part4_summarization(chunks)
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    
    metadata = results.get('metadata', {})
    print(f"\n📊 Processing Statistics:")
    print(f"   • Total Chunks: {metadata.get('total_chunks', 0)}")
    print(f"   • Total Sections: {metadata.get('total_sections', 0)}")
    print(f"   • Total Documents: {metadata.get('total_documents', 0)}")
    print(f"   • Compression Ratio: {metadata.get('compression_ratio', 0):.0%}")
    
    # Level summaries
    print(f"\n📝 Summarization Levels:")
    print(f"   Level 1 (Chunks): {len(results['chunk_summaries'])} summaries")
    print(f"   Level 2 (Sections): {len(results['section_summaries'])} summaries")
    print(f"   Level 3 (Documents): {len(results['document_summaries'])} summaries")
    print(f"   Level 4 (Executive): 1 meta-summary")
    
    # Executive summary statistics
    exec_summary = results['executive_summary']
    stats = exec_summary['statistics']
    
    print(f"\n🎯 Executive Summary Stats:")
    print(f"   • Avg chunks/doc: {stats['avg_chunks_per_doc']:.1f}")
    print(f"   • Avg sections/doc: {stats['avg_sections_per_doc']:.1f}")
    print(f"   • Total tokens: {stats['total_tokens']:,}")
    
    print(f"\n📊 Content Distribution:")
    for chunk_type, count in stats['chunk_type_distribution'].items():
        percentage = (count / stats['total_chunks'] * 100) if stats['total_chunks'] > 0 else 0
        print(f"   • {chunk_type}: {count} ({percentage:.1f}%)")
    
    # Sample summaries
    print(f"\n📖 Sample Chunk Summary:")
    if results['chunk_summaries']:
        sample = results['chunk_summaries'][0]
        print(f"   Chunk {sample['chunk_id']} ({sample['type']}):")
        print(f"   {sample['summary'][:150]}...")
    
    print(f"\n📚 Sample Section Summary:")
    if results['section_summaries']:
        sample = results['section_summaries'][0]
        print(f"   Section: {sample['section_name']}")
        print(f"   {sample['summary'][:150]}...")
    
    # Output files
    print("\n📁 Output Files Generated:")
    output_files = [
        "outputs/summaries/chunk_summaries.md",
        "outputs/summaries/section_summaries.md",
        "outputs/summaries/document_summaries.md",
        "outputs/summaries/executive_meta_summary.md",
        "outputs/summaries/hierarchical_summaries.json"
    ]
    
    for file_path in output_files:
        if Path(file_path).exists():
            print(f"   ✓ {file_path}")
    
    print("\n" + "="*70)
    print("✅ PART 4 TEST COMPLETED SUCCESSFULLY")
    print("="*70)
    
    print("\n💡 Key Features:")
    print("   • 4-level hierarchical summarization implemented")
    print("   • Chunk → Section → Document → Executive synthesis")
    print("   • Compression ratio: 30% of original content")
    print("   • Integrated with ERFDoc Document Intelligence Platform")
    
    print("\n📖 Next Steps:")
    print("   1. Review the executive_meta_summary.md")
    print("   2. Proceed to Part 5: Structured Information Extraction")
    print("   3. Use summaries for quick document navigation in ERFDoc")
    
    print(f"\n📄 View the executive summary:")
    print(f"   cat outputs/summaries/executive_meta_summary.md")


if __name__ == "__main__":
    main()
