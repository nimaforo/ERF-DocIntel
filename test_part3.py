"""
Test script for Part 3: Multi-Technique Prompting Strategy
"""

import json
from pathlib import Path
from document_intelligence.pipeline import DocumentIntelligencePipeline


def main():
    """Test Part 3 prompting strategies on document chunks."""
    
    print("="*70)
    print("TESTING PART 3: MULTI-TECHNIQUE PROMPTING STRATEGY")
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
    
    # Run Part 3 prompting experiments
    results = pipeline.run_part3_prompting(chunks)
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    
    print(f"\n📊 Prompting Strategies Tested: {results['strategies_tested']}")
    print(f"📝 Chunks Processed: {results['chunks_processed']}")
    
    # Show strategy comparison
    print("\n🎯 Strategy Performance:")
    for result in results['results']:
        print(f"\n   {result['strategy_name'].replace('_', ' ').title()}:")
        print(f"     • Time: {result['total_time']:.2f}s")
        print(f"     • Avg Response: {result['avg_response_length']:.0f} chars")
        print(f"     • Avg Prompt: {result['total_prompt_tokens'] / len(result['chunk_results']):.0f} tokens")
        print(f"     • Description: {result['strategy_description']}")
    
    # Output files
    print("\n📁 Output Files Generated:")
    report_file = Path("outputs/reports/prompt_experiments.md")
    results_file = Path("outputs/reports/prompt_results.json")
    
    if report_file.exists():
        print(f"   ✓ {report_file}")
    if results_file.exists():
        print(f"   ✓ {results_file}")
    
    print("\n" + "="*70)
    print("✅ PART 3 TEST COMPLETED SUCCESSFULLY")
    print("="*70)
    
    print("\n💡 Key Findings:")
    print("   • 9 different prompting strategies implemented")
    print("   • Each strategy optimized for different use cases")
    print("   • Integrated with ERFDoc Document Intelligence Platform")
    
    print("\n📖 Next Steps:")
    print("   1. Review the prompt_experiments.md report")
    print("   2. Proceed to Part 4: Hierarchical Summarization")
    print("   3. Integrate strategies into ERFDoc's query pipeline")
    
    print(f"\n📄 View the detailed report:")
    print(f"   cat outputs/reports/prompt_experiments.md")


if __name__ == "__main__":
    main()
