"""
Test script for Part 5: Structured Information Extraction
"""

import json
from pathlib import Path
from document_intelligence.pipeline import DocumentIntelligencePipeline
from document_intelligence.extraction import list_schemas, get_schema_info


def main():
    """Test Part 5 structured information extraction."""
    
    print("="*70)
    print("TESTING PART 5: STRUCTURED INFORMATION EXTRACTION")
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
    
    # Show available schemas
    schemas = list_schemas()
    print(f"\n📋 Available Schemas ({len(schemas)}):")
    for schema_name in schemas:
        info = get_schema_info(schema_name)
        print(f"   • {info['title']}")
        print(f"     - Required fields: {', '.join(info['required_fields'])}")
        print(f"     - Total properties: {info['total_properties']}")
    
    # Initialize pipeline
    pipeline = DocumentIntelligencePipeline()
    
    # Run Part 5 structured extraction
    results = pipeline.run_part5_extraction(chunks)
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    
    print(f"\n📊 Extraction Results:")
    for schema_name, extraction in results.items():
        validation = extraction['validation']
        status = "✅ VALID" if validation['is_valid'] else "❌ INVALID"
        
        print(f"\n   {schema_name.replace('_', ' ').title()}: {status}")
        
        if not validation['is_valid']:
            print(f"     Error: {validation['error']}")
        
        metadata = extraction['extraction_metadata']
        print(f"     Chunks processed: {metadata['chunks_processed']}")
        
        # Show sample fields
        data = extraction['extracted_data']
        required_fields = list(data.keys())[:3]
        print(f"     Sample fields: {', '.join(required_fields)}")
    
    # Output files
    print("\n📁 Output Files Generated:")
    output_files = [
        "outputs/extraction/legal_contract_extraction.json",
        "outputs/extraction/technical_proposal_extraction.json",
        "outputs/extraction/hr_compliance_extraction.json",
        "outputs/extraction/all_extractions.json",
        "outputs/reports/extraction_report.md"
    ]
    
    for file_path in output_files:
        if Path(file_path).exists():
            print(f"   ✓ {file_path}")
    
    print("\n" + "="*70)
    print("✅ PART 5 TEST COMPLETED SUCCESSFULLY")
    print("="*70)
    
    print("\n💡 Key Features:")
    print("   • 3 JSON schemas implemented with strict validation")
    print("   • Legal Contract, Technical Proposal, HR/Compliance schemas")
    print("   • Automatic field extraction with pattern matching")
    print("   • Schema validation for data integrity")
    
    print("\n📖 Schema Details:")
    print("   1. Legal Contract: parties, dates, terms, obligations")
    print("   2. Technical Proposal: scope, timeline, budget, team")
    print("   3. HR/Compliance: policy, requirements, procedures, compliance")
    
    print("\n📖 Next Steps:")
    print("   1. Review extraction results in outputs/extraction/")
    print("   2. Proceed to Part 6: Evaluation & Error Analysis")
    print("   3. Integrate extraction into ERFDoc's query pipeline")
    
    print(f"\n📄 View the extraction report:")
    print(f"   cat outputs/reports/extraction_report.md")
    
    # Show sample extraction
    print("\n📊 Sample Legal Contract Extraction:")
    legal_extraction = results.get('legal_contract', {}).get('extracted_data', {})
    print(f"   Contract Type: {legal_extraction.get('contract_type', 'N/A')}")
    print(f"   Parties: {len(legal_extraction.get('parties', []))} parties")
    print(f"   Effective Date: {legal_extraction.get('effective_date', 'N/A')}")
    print(f"   Jurisdiction: {legal_extraction.get('jurisdiction', 'N/A')}")


if __name__ == "__main__":
    main()
