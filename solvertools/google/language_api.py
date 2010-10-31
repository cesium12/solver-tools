# -*- coding: utf-8 -*-
import urllib, urllib2, json
from solvertools.lib.tokenize import tokenize_list, untokenize_list
from solvertools.lib.iso639 import langs

REFERER = 'http://manicsages.org'
API_ROOT = 'http://ajax.googleapis.com/ajax/services/language/'

def _quote_text(text):
    if isinstance(text, unicode):
        text = text.encode('utf-8')
    return urllib.quote(text)

def language_api_call(method, version, input, source_lang='', target_lang=''):
    query = '%s?v=%s&q=%s&langpair=%s%%7C%s' % (
        urllib.quote(method),
        urllib.quote(version),
        _quote_text(input),
        urllib.quote(source_lang),
        urllib.quote(target_lang)
    )
    url = API_ROOT + query
    req = urllib2.Request(url)

    # yes, this is how HTTP spells "referrer"
    req.add_header('Referer', REFERER)
    response = json.load(urllib2.urlopen(req))
    if response['responseStatus'] != 200:
        raise urllib2.HTTPError(url, response['responseStatus'],
        response['responseDetails'], {}, None)
    return response['responseData']

def translate(text, source_lang, target_lang):
    response = language_api_call('translate', '1.0', text, source_lang,
    target_lang)

    return response['translatedText']

def transliterate_word(word, source_lang, target_lang):
    response = language_api_call('transliterate', '1.0', word, source_lang,
    target_lang)
    return response['transliterations'][0]['transliteratedWords'][0]

def transliterate(text, source_lang, target_lang):
    trans = []
    for word in tokenize_list(text):
        trans.append(transliterate_word(word, source_lang, target_lang))
    return untokenize_list(trans)

def detect_language(text):
    response = language_api_call('detect', '1.0', text)
    return response['language'], response['confidence']

def auto_translate(text, target_lang):
    source_lang, confidence = detect_language(text)
    return translate(text, source_lang, target_lang)

def to_english(text):
    try:
        return auto_translate(text, 'en')
    except urllib2.HTTPError, e:
        if e.code == 400:
            lang, confidence = detect_language(text)
            return "(something in %s)" % langs.english_name(lang)
        else: raise

def demo():
    print translate('hello world', 'en', 'ja')
    print transliterate('hello world', 'en', 'ru')
    print to_english(translate('hello world', 'en', 'ja'))
    print to_english(u"नमस्ते")

if __name__ == '__main__': demo()

