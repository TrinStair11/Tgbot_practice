from googletrans import Translator

translator = Translator()


def translate_text(text, src, dest):
    try:
        translation = translator.translate(text=text, src=src, dest=dest)
        return translation.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return None
