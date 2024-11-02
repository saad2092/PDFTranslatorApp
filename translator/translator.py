# translator/translator.py

from googletrans import Translator


class TranslatorService:
    def __init__(self):
        self.translator = Translator()

    def translate_text(self, text, target_lang='en'):
        try:
            if text.strip() == '':
                return ''
            translation = self.translator.translate(text, dest=target_lang)
            return translation.text
        except Exception as e:
            return f'Error during translation: {e}'
