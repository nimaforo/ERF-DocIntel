# Setup Instructions - Complete Configuration Guide

## Quick Start (Already Done)

Your application has been fixed for the network error. Here's what was corrected:

✅ Fixed hardcoded OpenAI provider -> Now uses Ollama by default  
✅ Fixed Ollama URL for local development -> localhost:11434  
✅ Added error handling and retry logic -> Connection stability  
✅ Fixed model name -> qwen2.5:7b (matches installed model)  
✅ Added comprehensive logging -> Easier troubleshooting  

## Current Configuration

Your `.env` file is now set up for local development:

```env
MODEL_PROVIDER=local           # Uses Ollama
OLLAMA_BASE_URL=http://localhost:11434
LOCAL_MODEL_NAME=qwen2.5:7b   # Installed model
TEMPERATURE=0.3
MAX_TOKENS=4000
```

## Verifying Your Setup

### 1. Check Ollama Status
```bash
ollama list
# Should show: qwen2.5:7b
```

### 2. Check if Ollama is Running
```bash
python test_network_fix.py
# Should show: ✓ All tests passed!
```

### 3. Run a Test Query
```bash
python test_model_fix.py
# Should process a query successfully
```

## Running the Application

### Option A: Command Line Testing
```bash
python main.py
```

### Option B: Streamlit UI (ERFDoc)
```bash
streamlit run app/erfdoc_app.py
```

### Option C: Docker (Production)
```bash
# Update .env for Docker environment:
# OLLAMA_BASE_URL=http://host.docker.internal:11434

docker-compose up --build
```

## Troubleshooting

### Issue: "Cannot connect to Ollama"
1. Verify Ollama is running: `ollama list`
2. Check URL in .env matches: `http://localhost:11434`
3. Test connectivity: `python test_network_fix.py`

### Issue: "Model requires more memory"
This is a system limitation, not a code issue. Options:
1. Free up RAM by closing other applications
2. Use a smaller model:
   ```bash
   ollama pull mistral:latest
   # Update .env: LOCAL_MODEL_NAME=mistral:latest
   ```
3. Increase Docker's memory allocation (if using Docker)

### Issue: "Model not found"
1. Check installed models: `ollama list`
2. Update `.env` LOCAL_MODEL_NAME to match an installed model
3. Pull a model: `ollama pull mistral` or `ollama pull neural-chat`

### Issue: "DNS resolution failed" (getaddrinfo)
This was the original issue - it's fixed! But if it happens again:
1. Verify MODEL_PROVIDER=local in .env
2. Check OLLAMA_BASE_URL=http://localhost:11434
3. Run test: `python test_network_fix.py`

## Environment Variables Reference

| Variable | Default | Purpose |
|----------|---------|---------|
| MODEL_PROVIDER | local | Which LLM to use: local, openai, or anthropic |
| OLLAMA_BASE_URL | http://localhost:11434 | Ollama service endpoint |
| LOCAL_MODEL_NAME | qwen2.5:7b | Model name to use with Ollama |
| OPENAI_API_KEY | (not set) | Required if MODEL_PROVIDER=openai |
| ANTHROPIC_API_KEY | (not set) | Required if MODEL_PROVIDER=anthropic |
| TEMPERATURE | 0.3 | LLM response randomness |
| MAX_TOKENS | 4000 | Max response length |
| CHUNK_SIZE | 2000 | Document chunk size for processing |

## File Structure

```
project/
├── .env                          # Configuration (UPDATED)
├── config.py                     # Config module (UPDATED)
├── graph/
│   ├── agents.py                # Agent definitions (UPDATED)
│   ├── workflow.py              # LangGraph workflow (UPDATED)
│   └── state.py                 # Agent state
├── app/
│   ├── erfdoc_app.py            # Streamlit app
│   └── erfdoc_app.py            # Streamlit app
├── utils/
│   ├── hybrid_retriever.py
│   ├── translation_service.py
│   └── smart_translation.py
├── document_intelligence/       # Advanced processing
├── ingestion/
│   └── index.py                 # Document processor
├── test_network_fix.py          # (NEW) Network verification
└── test_model_fix.py            # (NEW) Model verification
```

## Testing Checklist

- [ ] Ollama running: `ollama list` shows available models
- [ ] Network test passes: `python test_network_fix.py` → All 5 tests pass
- [ ] Model test passes: `python test_model_fix.py` → Response received
- [ ] UI loads: `streamlit run app/erfdoc_app.py` → Opens in browser
- [ ] Query works: Send a test message in UI → Receives response

## Performance Tips

1. **Keep Ollama running**: Start once, keep in background
2. **Monitor memory**: First query may be slow (model loading), subsequent queries are fast
3. **Close unused apps**: Free up RAM for better performance
4. **Use web interface**: Streamlit provides cleaner UX than command line

## Support

If you encounter issues:
1. Check logs in terminal output
2. Run `python test_network_fix.py` for diagnosis
3. Verify all tests in the checklist above pass
4. Check that .env variables match your environment

## What Changed

**Network Error Root Cause**: Hardcoded OpenAI provider with no Ollama fallback  
**Solution**: Dynamic provider selection with proper error handling  
**Result**: Application now properly uses local Ollama service without network errors  

Your system is now configured correctly! 🎉
