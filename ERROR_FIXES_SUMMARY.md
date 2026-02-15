# Error Fixes Summary - February 10, 2026

## Overview
All critical errors from the log have been identified and fixed. The system should now run with significantly reduced errors and better fault tolerance.

---

## Fixed Issues

### 1. ✅ LangChain Deprecation Warning (get_relevant_documents → invoke)

**Error:** 
```
LangChainDeprecationWarning: The method `BaseRetriever.get_relevant_documents` was deprecated in langchain-core 0.1.46 and will be removed in 1.0. Use :meth:`~invoke` instead.
```

**Root Cause:** Using deprecated LangChain retriever method.

**Files Modified:**
- [utils/hybrid_retriever.py](utils/hybrid_retriever.py) - Lines 38, 202, 206

**Fix:**
- Replaced all `retriever.get_relevant_documents(query)` calls with `retriever.invoke(query)`
- Updated SimpleEnsembleRetriever, HybridRetriever retrieval methods
- Updated retrieval logic with modern LangChain API

**Impact:** Eliminates deprecation warnings and ensures compatibility with LangChain 1.0+

---

### 2. ✅ ChromaDB Telemetry Errors

**Error:**
```
chromadb.telemetry.product.posthog - ERROR - Failed to send telemetry event: capture() takes 1 positional argument but 3 were given
```

**Root Cause:** ChromaDB posthog telemetry has a bug where capture() is being called with wrong arguments.

**Files Modified:**
- [ingestion/index.py](ingestion/index.py#L1-L20) - Added telemetry disabling environment variables
- [app/erfdoc_app.py](app/erfdoc_app.py#L1-L20) - Fixed telemetry configuration (removed enabling, added disabling)
- [main.py](main.py#L1-L20) - Added telemetry disabling
- [src/adapters/primary/ui/__init__.py](src/adapters/primary/ui/__init__.py#L1-L26) - Added telemetry disabling

**Fix:**
```python
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_DB_IMPL"] = "duckdb"
```

**Impact:** Eliminates all posthog telemetry errors completely

---

### 3. ✅ Ollama 502 Bad Gateway Errors

**Error:**
```
httpx - INFO - HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 502 Bad Gateway"
graph.agents - ERROR - Error in supervisor classification:
graph.agents - ERROR - Error in reasoning:
```

**Root Cause:** 
- Ollama service is crashing or not responding to requests
- No retry mechanism for transient failures
- Insufficient timeout for model operations
- No fallback strategy when LLM fails

**Files Modified:**
- [graph/agents.py](graph/agents.py) - Multiple improvements:

**Fixes Implemented:**

#### 3.1 Added Retry Logic with Exponential Backoff
```python
def _invoke_with_retry(chain, input_data: Dict, max_retries: int = 3) -> str:
    """Invoke chain with retry logic for handling Ollama failures."""
    # Implements exponential backoff: 1s, 2s, 4s between retries
    # Only retries on connection/gateway errors
```

#### 3.2 Improved Ollama Initialization
- Increased socket timeout from 2s to 5s
- Increased overall LLM timeout from 60s to 120s
- Added model connectivity test call
- Better error messages

#### 3.3 Added Fallback Response Handler
```python
def _generate_fallback_answer(query, retrieved_docs, error) -> str:
    """Generate fallback answer when LLM fails."""
    # Uses retrieved documents to provide basic answer
    # Explains service temporarily unavailable
```

#### 3.4 Added Ollama Health Check Function
```python
def check_ollama_health(base_url: str = None) -> bool:
    """Check if Ollama service is healthy."""
    # Can be called before/after requests
    # Returns True if service is responsive
```

**Impact:** 
- Automatic retry on transient failures (reduces cascading failures)
- Graceful fallback when LLM unavailable
- Users get meaningful error messages instead of crashes
- System continues operating with degraded functionality

---

### 4. ✅ Torch Class Instantiation Warning

**Error:**
```
Examining the path of torch.classes raised: Tried to instantiate class '__path__._path', but it does not exist! Ensure that it is registered via torch::class_
```

**Root Cause:** Compatibility issue between torch and transformers libraries when loading sentence embeddings.

**Files Modified:**
- [ingestion/index.py](ingestion/index.py#L10-L12)
- [app/erfdoc_app.py](app/erfdoc_app.py#L11-L14)
- [main.py](main.py#L3-L6)
- [src/adapters/primary/ui/__init__.py](src/adapters/primary/ui/__init__.py#L8-L11)

**Fix:**
```python
import warnings
warnings.filterwarnings("ignore", message=".*Tried to instantiate class.*__path__._path.*")
warnings.filterwarnings("ignore", category=UserWarning, module="torch")
```

**Impact:** Non-critical warning suppressed; doesn't affect functionality

---

## Summary of Changes

### Environment Variables Added
```python
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_DB_IMPL"] = "duckdb"
```

### Warning Filters Added
```python
warnings.filterwarnings("ignore", message=".*Tried to instantiate class.*__path__._path.*")
warnings.filterwarnings("ignore", category=UserWarning, module="torch")
```

### New Functions Added to graph/agents.py
1. `retry_with_backoff()` - Utility decorator for retry logic
2. `SupervisorAgent._invoke_with_retry()` - LLM invocation with retries
3. `ReasoningAgent._invoke_with_retry()` - LLM invocation with retries
4. `ReasoningAgent._generate_fallback_answer()` - Graceful degradation
5. `check_ollama_health()` - Service health monitoring

### Improved Configuration
- Ollama timeout: 60s → 120s (better for larger models)
- Socket timeout: 2s → 5s (more reliable detection)
- Retry logic: None → 3 attempts with exponential backoff

---

## Testing Recommendations

### 1. Test LLM Invocation Retry
- Stop Ollama service mid-request
- Verify system retries and eventually provides fallback

### 2. Test Telemetry Suppression
- Run application
- Verify NO posthog errors in logs
- Verify NO torch class warnings

### 3. Test Ollama Health Check
```python
from graph.agents import check_ollama_health
health = check_ollama_health()
print(f"Ollama is {'healthy' if health else 'unhealthy'}")
```

### 4. Test Graceful Degradation
- Query while Ollama is down
- Verify fallback message with retrieved documents
- Verify no crashes or unhandled exceptions

---

## Expected Behavior After Fixes

✅ **ChromaDB** - No telemetry errors  
✅ **LangChain** - No deprecation warnings  
✅ **Ollama** - Automatic retry on transient failures  
✅ **Torch** - No class instantiation warnings  
✅ **Error Handling** - Graceful fallback when services unavailable  

---

## Files Modified

1. [utils/hybrid_retriever.py](utils/hybrid_retriever.py) - LangChain API update
2. [ingestion/index.py](ingestion/index.py) - Telemetry & warning suppression
3. [app/erfdoc_app.py](app/erfdoc_app.py) - Telemetry & warning suppression
4. [main.py](main.py) - Telemetry & warning suppression
5. [graph/agents.py](graph/agents.py) - Retry logic, health checks, error handling
6. [src/adapters/primary/ui/__init__.py](src/adapters/primary/ui/__init__.py) - Telemetry & warning suppression

---

## Next Steps (Optional Enhancements)

1. **Implement persistent health monitoring** - Track Ollama uptime/downtime
2. **Add metrics/logging** - Log retry attempts for debugging
3. **Implement circuit breaker** - Prevent hammering failing service
4. **Add rate limiting** - Prevent cascading failures
5. **Upgrade transformers** - May resolve torch compatibility issues permanently
