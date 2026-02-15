"""
Test script for Part 6: Evaluation & Error Analysis
"""

import json
from pathlib import Path
from document_intelligence.pipeline import DocumentIntelligencePipeline


def main():
    """Test Part 6 evaluation and error analysis."""
    
    print("="*70)
    print("TESTING PART 6: EVALUATION & ERROR ANALYSIS")
    print("="*70)
    
    # Check prerequisites
    required_files = [
        Path("outputs/summaries/hierarchical_summaries.json"),
        Path("outputs/extraction/legal_contract_extraction.json"),
        Path("outputs/processed_documents.json")
    ]
    
    print("\n📋 Checking prerequisites...")
    for file_path in required_files:
        status = "✓" if file_path.exists() else "✗"
        print(f"   {status} {file_path}")
    
    # Initialize pipeline
    pipeline = DocumentIntelligencePipeline()
    
    # Run Part 6 evaluation
    results = pipeline.run_part6_evaluation()
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    
    # Summarization results
    if results.get("summarization"):
        print("\n📊 Summarization Quality (ROUGE-L):")
        for result in results["summarization"]:
            avg = result["average_scores"]
            print(f"   • Samples evaluated: {result['samples_evaluated']}")
            print(f"   • Precision: {avg['precision']:.4f}")
            print(f"   • Recall: {avg['recall']:.4f}")
            print(f"   • F1: {avg['f1']:.4f}")
    
    # Extraction results
    if results.get("extraction"):
        print("\n📊 Extraction Accuracy (Precision/Recall):")
        for result in results["extraction"]:
            scores = result["scores"]
            print(f"   • Precision: {scores['precision']:.4f}")
            print(f"   • Recall: {scores['recall']:.4f}")
            print(f"   • F1: {scores['f1']:.4f}")
            print(f"   • TP: {scores['true_positives']}, FP: {scores['false_positives']}, FN: {scores['false_negatives']}")
    
    # OCR results
    if results.get("ocr"):
        print("\n📊 OCR Quality (CER/WER):")
        for result in results["ocr"]:
            avg = result["average_scores"]
            print(f"   • Samples evaluated: {result['samples_evaluated']}")
            print(f"   • Character Error Rate (CER): {avg['cer']:.4f}")
            print(f"   • Word Error Rate (WER): {avg['wer']:.4f}")
    
    # Output files
    print("\n📁 Output Files Generated:")
    output_files = [
        "outputs/reports/evaluation_report.md",
        "outputs/evaluation/evaluation_results.json",
        "outputs/evaluation/annotations/annotations.json",
        "outputs/evaluation/annotation_template.json"
    ]
    
    for file_path in output_files:
        if Path(file_path).exists():
            print(f"   ✓ {file_path}")
    
    print("\n" + "="*70)
    print("✅ PART 6 TEST COMPLETED SUCCESSFULLY")
    print("="*70)
    
    print("\n💡 Key Features:")
    print("   • ROUGE-L for summarization quality")
    print("   • Precision/Recall for extraction accuracy")
    print("   • CER/WER for OCR quality")
    print("   • Manual annotation interface")
    print("   • Comprehensive evaluation reports")
    
    print("\n📊 Metrics Implemented:")
    print("   1. ROUGE-L: Longest Common Subsequence for summaries")
    print("   2. Precision/Recall/F1: Structured extraction accuracy")
    print("   3. CER: Character Error Rate for OCR")
    print("   4. WER: Word Error Rate for OCR")
    
    print("\n📖 Annotation Interface:")
    print("   • Create manual annotations for ground truth")
    print("   • Annotation template for easy data entry")
    print("   • Support for summaries, extractions, and OCR")
    
    print("\n📖 Next Steps:")
    print("   1. Review evaluation report in outputs/reports/")
    print("   2. Use annotation template to add ground truth data")
    print("   3. Proceed to Part 7: Final Reflection & Documentation")
    
    print(f"\n📄 View the evaluation report:")
    print(f"   cat outputs/reports/evaluation_report.md")
    
    # Show performance summary
    if results.get("summarization"):
        avg_f1 = results["summarization"][0]["average_scores"]["f1"]
        status = "Good" if avg_f1 >= 0.5 else "Needs Improvement"
        print(f"\n📈 Summarization Performance: {status} (F1={avg_f1:.3f})")
    
    if results.get("extraction"):
        ext_f1 = results["extraction"][0]["scores"]["f1"]
        status = "Good" if ext_f1 >= 0.7 else "Needs Improvement"
        print(f"📈 Extraction Performance: {status} (F1={ext_f1:.3f})")
    
    if results.get("ocr"):
        avg_cer = results["ocr"][0]["average_scores"]["cer"]
        status = "Excellent" if avg_cer <= 0.1 else "Acceptable" if avg_cer <= 0.2 else "Needs Improvement"
        print(f"📈 OCR Performance: {status} (CER={avg_cer:.3f})")


if __name__ == "__main__":
    main()
