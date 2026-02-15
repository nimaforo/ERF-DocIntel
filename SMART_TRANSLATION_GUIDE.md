# Smart Translation System - User Guide

## Overview
The application now features an **intelligent translation system** that automatically detects when translation is needed and uses **LLM supervision** to improve translation quality.

## Key Features

### 1. **Automatic Language Detection**
The system automatically detects the language of your prompts:
- **Persian/Farsi** (فارسی)
- **English**
- **Arabic** (العربية)

### 2. **Smart Translation Intent Analysis**
The system intelligently determines:
- Whether your prompt needs translation before processing
- Whether the output needs translation
- What language you want the response in

### 3. **LLM-Supervised Translation**
All translations now use **dual-layer processing**:
1. **Google Translate** provides initial translation
2. **LLM (AI)** reviews and improves the translation for naturalness and accuracy

This results in much higher quality translations compared to Google Translate alone.

## How It Works

### Example 1: Persian Prompt → Persian Response
```
You type (in Persian): این سند درباره چیست؟
System automatically:
  1. Detects Persian language
  2. Translates to English: "What is this document about?"
  3. Processes with LLM in English
  4. Translates response back to Persian (with LLM supervision)
```

### Example 2: English Prompt with Language Request
```
You type: "Tell me about this document in Farsi"
System automatically:
  1. Detects: English prompt requesting Persian output
  2. Processes prompt in English
  3. Translates response to Persian (with LLM supervision)
```

### Example 3: Mixed Request
```
You type (in Persian): به انگلیسی توضیح بده
System automatically:
  1. Detects: Persian prompt requesting English output
  2. Translates prompt to English
  3. Returns response in English (no translation needed)
```

## Supported Language Request Patterns

The system recognizes these patterns in your prompts:

### For Persian Output:
- "in Farsi" or "in Persian"
- "to Farsi" or "to Persian"
- "به فارسی"
- "در فارسی"
- "فارسی بگو"

### For English Output:
- "in English"
- "to English"
- "به انگلیسی"

### For Arabic Output:
- "in Arabic"
- "به عربی"

## Manual Translation Controls

You can still manually control translation using the sidebar:

### Translation Options:
1. **🚫 No Translation** - Default behavior (smart translation still active)
2. **🔄 English → Persian** - Force English to Persian translation
3. **🔄 Persian → English** - Force Persian to English translation
4. **✨ Rephrase (English)** - Use LLM to rephrase in clearer English
5. **✨ Rephrase (Persian)** - Use LLM to rephrase in clearer Persian

## Translation Flow

```
┌─────────────────┐
│  User Prompt    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Detect Language &       │
│ Translation Intent      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Translate Prompt if     │
│ needed (non-English)    │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Process with LLM        │
│ (in English)            │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ LLM-Supervised          │
│ Translation if needed   │
│ (Google + LLM Review)   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Display Response        │
└─────────────────────────┘
```

## LLM Supervision Process

When translating output:

1. **Google Translate** creates initial translation
2. **LLM Reviews** the translation and checks for:
   - Accuracy of meaning
   - Natural language flow
   - Cultural appropriateness
   - Context preservation
3. **LLM Improves** the translation if needed
4. **Final translation** is returned to user

This ensures high-quality, natural-sounding translations.

## Benefits

### For Users:
- ✅ No need to manually select translation - it's automatic
- ✅ Can ask questions in your native language
- ✅ Can request specific output language in your prompt
- ✅ Much better translation quality with LLM supervision

### For Developers:
- ✅ Centralized translation logic in `SmartTranslationHandler`
- ✅ Easy to extend with new language patterns
- ✅ Consistent translation quality across the app
- ✅ Logging and debugging of translation decisions

## Technical Details

### New Files:
- **`utils/smart_translation.py`** - Smart translation handler
  - `SmartTranslationHandler` class
  - `TranslationIntent` dataclass
  - Language request pattern detection

### Enhanced Files:
- **`utils/translation_service.py`**
  - `translate_with_llm_supervision()` method
  - Dual-layer translation (Google + LLM)

- **`app/erfdoc_app.py`** (primary application)
  - Integration with smart translation handler
  - Automatic prompt translation
  - Automatic output translation

### Key Classes:

#### `TranslationIntent`
Stores detected translation intent:
```python
@dataclass
class TranslationIntent:
    prompt_language: str
    requested_output_language: Optional[str]
    needs_prompt_translation: bool
    needs_output_translation: bool
    output_target_language: Optional[str]
    confidence: float
    reason: str
```

#### `SmartTranslationHandler`
Main handler for intelligent translation:
```python
handler = SmartTranslationHandler(translation_service)

# Analyze prompt
intent = handler.analyze_prompt(
    prompt="درباره این سند بگو",
    app_mode="chat",
    user_selected_translation="none"
)

# Translate prompt if needed
translated_prompt = handler.translate_prompt_if_needed(
    prompt="درباره این سند بگو",
    intent=intent
)

# Translate output if needed
translated_output = handler.translate_output_if_needed(
    output="This document discusses...",
    intent=intent,
    llm_agent=agent  # For LLM supervision
)
```

## Examples

### Example 1: Automatic Persian Detection
```
Input: "این سند چیست؟"
Detection: Persian prompt detected
Action: Translate to English → Process → Translate back to Persian
Output: (Persian response about the document)
```

### Example 2: Language Request in Prompt
```
Input: "Summarize this document in Farsi"
Detection: English prompt, Persian output requested
Action: Process in English → Translate to Persian
Output: (Persian summary)
```

### Example 3: No Translation Needed
```
Input: "What is this document?"
Detection: English prompt, no language request
Action: Process in English → Return in English
Output: (English response)
```

## Logging

Translation decisions are logged for debugging:
```
INFO: Translation intent: Persian prompt detected, translating to English for processing, will translate response back to Persian
INFO: Translated prompt from fa to English
INFO: Translating output to fa
INFO: Requesting LLM supervision for fa → en translation
INFO: LLM supervision completed successfully
```

## Configuration

No configuration needed! The system works automatically.

However, you can still use manual translation controls in the sidebar for specific cases.

## Future Enhancements

Potential future improvements:
- Support for more languages (Spanish, French, etc.)
- Context-aware translation (technical vs. casual)
- Translation quality feedback system
- Cache LLM-supervised translations
- Multi-model translation ensemble

## Troubleshooting

**Issue**: Translation not working
- Check that LLM agent is initialized
- Check logs for error messages
- Try manual translation mode

**Issue**: Wrong language detected
- Use manual translation mode
- Report the prompt pattern for improvement

**Issue**: Low translation quality
- LLM supervision should improve quality
- Can use "Rephrase" mode for better results

## Support

For issues or questions about the smart translation system:
1. Check the logs in the console
2. Try manual translation mode as fallback
3. Review this documentation
4. Contact the development team
