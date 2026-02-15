"""
Quick demo of cache performance
"""

from document_intelligence.integration import DocumentIntelligenceIntegration
from pathlib import Path
import time

di = DocumentIntelligenceIntegration()
pdf = Path('data/processed/Anti_cheat_for_video_games_final_07_03_2020.txt')

print('=' * 80)
print('CACHE PERFORMANCE DEMONSTRATION')
print('=' * 80)

# First processing (force reprocess)
print('\n[1] First Processing (Full Pipeline - forced reprocess)...')
start = time.time()
r1 = di.process_uploaded_document(pdf, False, force_reprocess=True)
t1 = time.time() - start
print(f'    Time: {t1:.2f}s')
print(f'    Status: {r1["status"]}')
print(f'    From cache: {r1.get("from_cache", False)}')

# Second processing (should use cache)
print('\n[2] Second Processing (Should Use Cache)...')
start = time.time()
r2 = di.process_uploaded_document(pdf, False, force_reprocess=False)
t2 = time.time() - start
print(f'    Time: {t2:.2f}s')
print(f'    Status: {r2["status"]}')
print(f'    From cache: {r2.get("from_cache", False)}')

# Show speedup
if t2 > 0:
    speedup = t1 / t2
    print(f'\n🚀 RESULT: {speedup:.1f}x faster with cache!')
else:
    print('\n🚀 Cache retrieval was instant!')

print('\n' + '=' * 80)
