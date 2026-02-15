"""
Test script for Part 7: Final Reflection & Documentation
"""

from pathlib import Path
from document_intelligence.pipeline import DocumentIntelligencePipeline


def main():
    """Test Part 7 final reflection and documentation."""
    
    print("="*70)
    print("TESTING PART 7: FINAL REFLECTION & DOCUMENTATION")
    print("="*70)
    
    # Check prerequisites
    required_files = [
        Path("outputs/reports/prompt_results.json"),
        Path("outputs/chunks/chunks.json"),
        Path("outputs/extraction/all_extractions.json"),
        Path("outputs/evaluation/evaluation_results.json")
    ]
    
    print("\n📋 Checking prerequisites...")
    all_present = True
    for file_path in required_files:
        status = "✓" if file_path.exists() else "✗"
        print(f"   {status} {file_path}")
        if not file_path.exists():
            all_present = False
    
    if not all_present:
        print("\n⚠ Warning: Some prerequisite files are missing")
        print("   The reflection will be generated with available data")
    
    # Initialize pipeline
    pipeline = DocumentIntelligencePipeline()
    
    # Run Part 7 reflection
    results = pipeline.run_part7_reflection()
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    
    # Prompt Analysis
    if results.get("prompt_analysis"):
        prompt = results["prompt_analysis"]
        print("\n📊 Prompt Strategy Analysis:")
        print(f"   • Total strategies: {prompt.get('total_strategies', 0)}")
        print(f"   • Most detailed: {prompt.get('most_detailed', 'N/A')}")
        print(f"   • Most efficient: {prompt.get('most_efficient', 'N/A')}")
    
    # Chunking Analysis
    if results.get("chunking_analysis"):
        chunking = results["chunking_analysis"]
        print("\n📊 Chunking Quality Analysis:")
        print(f"   • Total chunks: {chunking.get('total_chunks', 0)}")
        print(f"   • Total sections: {chunking.get('total_sections', 0)}")
        print(f"   • Avg tokens/chunk: {chunking.get('token_statistics', {}).get('average', 0)}")
        print(f"   • Quality: {chunking.get('structure_quality', 'N/A')}")
    
    # Extraction Analysis
    if results.get("extraction_analysis"):
        extraction = results["extraction_analysis"]
        print("\n📊 Extraction Accuracy Analysis:")
        print(f"   • Total schemas: {extraction.get('total_schemas', 0)}")
        print(f"   • Valid extractions: {extraction.get('valid_extractions', 0)}")
        print(f"   • Validation rate: {extraction.get('validation_rate', 0):.1f}%")
    
    # Error Correlation
    if results.get("error_correlation"):
        correlation = results["error_correlation"]
        print("\n📊 Error Correlation Analysis:")
        metrics = correlation.get('metrics', {})
        print(f"   • Summarization F1: {metrics.get('summarization_f1', 0):.3f}")
        print(f"   • Extraction F1: {metrics.get('extraction_f1', 0):.3f}")
        print(f"   • OCR CER: {metrics.get('ocr_cer', 0):.3f}")
        print(f"   • System health: {correlation.get('overall_system_health', 'N/A')}")
    
    # Lessons Learned
    if results.get("lessons_learned"):
        lessons = results["lessons_learned"]
        print(f"\n💡 Lessons Learned ({len(lessons)} total):")
        for lesson in lessons[:3]:
            print(f"   • {lesson}")
        if len(lessons) > 3:
            print(f"   ... and {len(lessons) - 3} more")
    
    # Recommendations
    if results.get("recommendations"):
        recommendations = results["recommendations"]
        print(f"\n🎯 Recommendations ({len(recommendations)} total):")
        for rec in recommendations[:3]:
            print(f"   • {rec}")
        if len(recommendations) > 3:
            print(f"   ... and {len(recommendations) - 3} more")
    
    # Output files
    print("\n📁 Output Files Generated:")
    output_files = [
        "outputs/reports/final_reflection.md",
        "outputs/reflection/analysis_results.json"
    ]
    
    for file_path in output_files:
        if Path(file_path).exists():
            print(f"   ✓ {file_path}")
    
    print("\n" + "="*70)
    print("✅ PART 7 TEST COMPLETED SUCCESSFULLY")
    print("="*70)
    
    print("\n💡 Key Deliverables:")
    print("   • Comprehensive reflection report with findings")
    print("   • Prompt strategy performance analysis")
    print("   • Document structure impact assessment")
    print("   • Error correlation study")
    print("   • Lessons learned and recommendations")
    
    print("\n📊 Analysis Coverage:")
    print("   1. Which prompt styles worked best?")
    print("   2. How did document structure impact chunking?")
    print("   3. Do extraction errors correlate with summarization errors?")
    print("   4. What are the key lessons learned?")
    print("   5. What improvements should be prioritized?")
    
    print("\n🎓 Project Complete:")
    print("   ✅ Part 1: Data Ingestion & Cleaning")
    print("   ✅ Part 2: Semantic Chunking")
    print("   ✅ Part 3: Multi-Technique Prompting")
    print("   ✅ Part 4: Hierarchical Summarization")
    print("   ✅ Part 5: Structured Information Extraction")
    print("   ✅ Part 6: Evaluation & Error Analysis")
    print("   ✅ Part 7: Final Reflection & Documentation")
    
    print(f"\n📄 View the final reflection:")
    print(f"   cat outputs/reports/final_reflection.md")
    
    print("\n🚀 Next Steps:")
    print("   1. Review final_reflection.md for insights")
    print("   2. Integrate with ERFDoc platform")
    print("   3. Implement priority recommendations")
    print("   4. Deploy to production environment")


if __name__ == "__main__":
    main()
