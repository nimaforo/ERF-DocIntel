"""
Clear document intelligence cache to force fresh processing with enhanced prompts.
Run this to see the difference in processing!
"""

import json
from pathlib import Path

def clear_cache():
    """Clear all document intelligence caches."""
    
    print("=" * 80)
    print("CLEARING DOCUMENT INTELLIGENCE CACHE")
    print("=" * 80)
    
    # Clear processed documents cache
    processed_file = Path("outputs/processed_documents.json")
    if processed_file.exists():
        with open(processed_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = len(data)
        print(f"\n✓ Found {count} cached documents")
        
        # Backup
        backup_file = Path("outputs/processed_documents_backup.json")
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Backup saved to: {backup_file}")
        
        # Clear
        with open(processed_file, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        print(f"✓ Cleared cache: {processed_file}")
    else:
        print("\n⚠️ No cache file found")
    
    # Show cached files that will be reprocessed
    output_dirs = {
        "chunks": Path("outputs/chunks"),
        "summaries": Path("outputs/summaries"),
        "extractions": Path("outputs/extraction"),
    }
    
    print("\n" + "=" * 80)
    print("Files that will be regenerated on next upload:")
    print("=" * 80)
    
    for name, path in output_dirs.items():
        if path.exists():
            files = list(path.glob("*.*"))
            if files:
                print(f"\n{name.upper()}:")
                for f in files[:5]:  # Show first 5
                    print(f"  - {f.name}")
                if len(files) > 5:
                    print(f"  ... and {len(files)-5} more")
    
    print("\n" + "=" * 80)
    print("✅ CACHE CLEARED!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Restart Docker: docker-compose restart")
    print("2. Upload a document at http://localhost:8501")
    print("3. Watch for enhanced processing with:")
    print("   - ✨ Role-based prompts")
    print("   - 📊 Advanced summarization strategies")
    print("   - 🎯 Better structured extraction")
    print("   - 📋 Executive summary preview in UI")
    print("\nYou'll see the difference! 🚀")


if __name__ == "__main__":
    clear_cache()
