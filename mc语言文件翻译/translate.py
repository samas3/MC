from deep_translator import *
def translate(text, lang, proxy=None):
    translated = GoogleTranslator(source='en', target=lang, proxies=proxy).translate(text)
    return translated
def remove_unprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())
if __name__ == '__main__':
    text = "Hello, world!"
    lang = "zh-CN"
    translated = translate(text, lang)
    print(translated)