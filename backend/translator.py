"""
Translation utility module for Chinese-English translation
Supports automatic language detection and bidirectional translation
"""

from deep_translator import GoogleTranslator
import re

# Unicode range for CJK Unified Ideographs (Chinese characters)
CJK_START = '\u4e00'
CJK_END = '\u9fff'

# Threshold for determining if text is primarily Chinese
# If Chinese characters make up more than this percentage, text is classified as Chinese
CHINESE_THRESHOLD = 0.3

class TranslationService:
    """Service for translating text between Chinese and English"""
    
    def __init__(self):
        self.translator = GoogleTranslator()
        self.supported_languages = ['zh-CN', 'en']
    
    def detect_language(self, text):
        """
        Detect the language of the input text
        
        Args:
            text: Input text to detect
            
        Returns:
            str: Language code ('zh-CN' or 'en')
        """
        try:
            # Remove whitespace for better detection
            text = text.strip()
            
            if not text:
                return 'en'
            
            # Simple heuristic: check for Chinese characters
            # Count Chinese characters using defined Unicode range
            chinese_chars = sum(1 for char in text if CJK_START <= char <= CJK_END)
            total_chars = len(text.replace(' ', ''))
            
            # If Chinese characters exceed threshold, consider it Chinese
            if total_chars > 0 and (chinese_chars / total_chars) > CHINESE_THRESHOLD:
                return 'zh-CN'
            else:
                return 'en'
                
        except Exception as e:
            print(f"Language detection error: {str(e)}")
            # Default to English if detection fails
            return 'en'
    
    def translate(self, text, target_lang=None, source_lang=None):
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code ('zh-CN' or 'en')
                        If None, automatically detect and translate to opposite language
            source_lang: Source language code (optional)
            
        Returns:
            dict: Translation result containing:
                - translated_text: The translated text
                - source_lang: Detected/provided source language
                - target_lang: Target language
                - original_text: Original input text
        """
        try:
            # Validate input
            if not text or not text.strip():
                return {
                    'translated_text': text,
                    'source_lang': 'unknown',
                    'target_lang': target_lang or 'en',
                    'original_text': text,
                    'error': 'Empty text provided'
                }
            
            # Detect source language if not provided
            if not source_lang:
                source_lang = self.detect_language(text)
            
            # Auto-determine target language if not provided
            if not target_lang:
                target_lang = 'en' if source_lang == 'zh-CN' else 'zh-CN'
            
            # Normalize language codes for deep-translator
            if target_lang.lower() in ['zh-cn', 'zh_cn', 'chinese']:
                target_lang = 'zh-CN'
            elif target_lang.lower() in ['en', 'english']:
                target_lang = 'en'
            
            if source_lang.lower() in ['zh-cn', 'zh_cn', 'chinese']:
                source_lang = 'zh-CN'
            elif source_lang.lower() in ['en', 'english']:
                source_lang = 'en'
            
            # Skip translation if source and target are the same
            if source_lang == target_lang:
                return {
                    'translated_text': text,
                    'source_lang': source_lang,
                    'target_lang': target_lang,
                    'original_text': text,
                    'skipped': True
                }
            
            # Perform translation using deep-translator
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated_text = translator.translate(text)
            
            return {
                'translated_text': translated_text,
                'source_lang': source_lang,
                'target_lang': target_lang,
                'original_text': text
            }
            
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return {
                'translated_text': text,
                'source_lang': source_lang or 'unknown',
                'target_lang': target_lang or 'en',
                'original_text': text,
                'error': str(e)
            }
    
    def batch_translate(self, texts, target_lang=None):
        """
        Translate multiple texts
        
        Args:
            texts: List of texts to translate
            target_lang: Target language code
            
        Returns:
            list: List of translation results
        """
        results = []
        for text in texts:
            result = self.translate(text, target_lang=target_lang)
            results.append(result)
        return results
