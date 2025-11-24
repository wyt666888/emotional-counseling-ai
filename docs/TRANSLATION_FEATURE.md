# Chinese-English Translation Feature

## Overview

This feature adds comprehensive Chinese-English bidirectional translation to the Emotional Counseling AI application. Users can enable real-time translation of all conversation messages with automatic language detection.

## Features

### 1. Automatic Language Detection
- Uses character-based heuristic analysis
- Identifies Chinese text based on CJK Unified Ideographs (Unicode U+4E00 to U+9FFF)
- Threshold: 30% Chinese characters → classified as Chinese
- High accuracy for mixed-language content

### 2. Real-time Translation
- Translates messages as they are sent/received
- Toggle translation on/off without losing conversation
- Displays both original and translated text
- Shows source and target language indicators

### 3. Manual Language Selection
- **Auto Mode**: Automatically detect language and translate to opposite language
- **Chinese (zh-CN)**: Force translation to Chinese
- **English (en)**: Force translation to English

### 4. Performance Optimization
- Batch translation: 3 messages per batch
- 500ms delay between batches to prevent rate limiting
- Lazy translation: only translates when enabled

## Technical Implementation

### Backend

#### Translation Service (`backend/translator.py`)
```python
class TranslationService:
    - detect_language(text) -> str
    - translate(text, target_lang, source_lang) -> dict
    - batch_translate(texts, target_lang) -> list
```

**Key Features:**
- Uses `deep-translator` library with Google Translate backend
- Language detection with configurable threshold
- Robust error handling (returns original text on failure)
- No API key required

#### API Endpoints

**POST /api/translate**
- Translates text between Chinese and English
- Auto-detects source language if not specified
- Returns translation with metadata

**POST /api/translate/detect**
- Detects language of input text
- Returns language code (zh-CN or en)

### Frontend

#### UI Components (`frontend/src/App.jsx`)

**Translation Controls:**
- Toggle button with Languages icon
- Language selector dropdown
- Visual indicator when translation is active

**Message Display:**
- Original text in primary color
- Translation below in secondary styling
- Language direction indicator (e.g., "zh-CN → en")
- Border separator between original and translation

#### State Management
```javascript
const [translationEnabled, setTranslationEnabled] = useState(false);
const [targetLanguage, setTargetLanguage] = useState('auto');
const [translatedMessages, setTranslatedMessages] = useState({});
```

## Usage

### For Users

1. **Enable Translation**
   - Click the "翻译" (Translation) button in the header
   - Button turns blue when active

2. **Select Target Language**
   - Choose from dropdown: Auto / 中文 / English
   - "Auto" translates to opposite language automatically

3. **View Translations**
   - Original message appears first
   - Translation appears below with language indicator
   - Both texts remain visible for reference

### For Developers

#### Testing Translation Service
```bash
cd backend
python -c "
from translator import TranslationService
service = TranslationService()

# Test detection
print(service.detect_language('你好'))  # zh-CN
print(service.detect_language('Hello'))  # en

# Test translation
result = service.translate('你好', target_lang='en')
print(result['translated_text'])
"
```

#### API Testing
```bash
# Test language detection
curl -X POST http://localhost:5000/api/translate/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，世界"}'

# Test translation (auto-detect)
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "I am happy"}'

# Test translation (manual target)
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "target_lang": "zh-CN"}'
```

## Configuration

### Backend Constants (`backend/translator.py`)
```python
# Unicode range for CJK Unified Ideographs
CJK_START = '\u4e00'
CJK_END = '\u9fff'

# Threshold for Chinese language detection (30%)
CHINESE_THRESHOLD = 0.3
```

### Frontend Settings (`frontend/src/App.jsx`)
```javascript
// Batch size for bulk translation
const batchSize = 3;

// Delay between batches (milliseconds)
const delay = 500;
```

## Architecture Decisions

### Why deep-translator?
- No API key required (uses Google Translate web interface)
- Simple, lightweight, and reliable
- Good for small to medium scale applications
- Easy to switch to paid service if needed

### Why Character-Based Detection?
- Fast and accurate for Chinese/English detection
- No external service calls required
- Works offline
- Simple and maintainable

### Why Batch Translation?
- Prevents API rate limiting
- Better user experience (gradual loading)
- Reduces server load
- Maintains UI responsiveness

## Limitations & Future Improvements

### Current Limitations
1. Requires internet connection for translation API
2. Limited to Chinese and English only
3. No offline translation support
4. Rate limiting on free Google Translate tier

### Potential Improvements
1. **Add More Languages**: Extend to support other languages
2. **Caching**: Cache translations to reduce API calls
3. **Offline Mode**: Use local translation model for basic phrases
4. **Translation Quality**: Add alternative translation providers (DeepL, Azure)
5. **Context Awareness**: Improve translation for emotion counseling domain
6. **Translation Memory**: Remember and reuse common translations

## Security Considerations

✅ **Input Validation**: All text is sanitized before translation
✅ **Error Handling**: Failed translations return original text
✅ **No Sensitive Data**: Translations don't store personal information
✅ **Rate Limiting**: Batched requests prevent abuse
✅ **XSS Prevention**: HTML escaped in utils.py before processing

## Troubleshooting

### Translation Not Working
1. Check internet connection
2. Verify backend server is running
3. Check browser console for errors
4. Test API endpoints directly with curl

### Incorrect Language Detection
1. Ensure text has sufficient length (>5 characters recommended)
2. Check CJK_THRESHOLD setting
3. Test with pure Chinese/English text first

### Performance Issues
1. Reduce batch size if too slow
2. Increase delay between batches
3. Consider caching frequently used translations
4. Check network latency

## Testing

### Unit Tests
```bash
# Test backend translation service
cd backend
python -m pytest test_translator.py  # (if created)
```

### Integration Tests
```bash
# Test API endpoints
python /path/to/test_backend_server.py
```

### Manual Testing Checklist
- [ ] Enable/disable translation toggle
- [ ] Switch between language modes (Auto/Chinese/English)
- [ ] Send Chinese message, verify English translation
- [ ] Send English message, verify Chinese translation
- [ ] Test with mixed content (Chinese + English)
- [ ] Test with emoji and special characters
- [ ] Verify translation persists during conversation
- [ ] Test batch translation with 10+ messages

## License

This feature is part of the Emotional Counseling AI project and is released under the MIT License.

## Credits

- **Translation Service**: [deep-translator](https://github.com/nidhaloff/deep-translator)
- **Icon**: Lucide React (Languages icon)
- **Implementation**: GitHub Copilot Coding Agent
