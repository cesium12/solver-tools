# -*- coding: utf-8 -*-
u"""
This module lets you interact with Google's astoundingly useful (and sometimes
hilarious) Language API. It can translate, transliterate, and detect the
language of arbitrary text.

Languages are represented as ISO 639 language codes, the abbreviations for a
language (usually two letters long) used in many standards.

If you want to know a particular language's code, look at the URL of the
Wikipedia in that language -- for example, the French Wikipedia is
"fr.wikipedia.org", so its language code is "fr".

Examples::

    # Translate "Hello World" to Japanese
    >>> print translate('hello world', 'en', 'ja')
    こんにちは世界
    
    # Approximately spell the English phrase "hello world"
    # in Cyrillic characters
    >>> print transliterate('hello world', 'en', 'ru')
    хелло ворлд

    # Try out our universal translator
    >>> print to_english(u"こんにちは世界")
    Hello World

    >>> print to_english(u"नमस्ते")
    (something in Sanskrit)

*Do not call these functions in a loop*. You might get us banned from using the
API. Google's rule is that every request has to be initiated by a user.
"""

import urllib, urllib2, json
from solvertools.lib.tokenize import tokenize_list, untokenize_list
from solvertools.lib.iso639 import langs

REFERER = 'http://manicsages.org'
API_ROOT = 'http://ajax.googleapis.com/ajax/services/language/'

class RequestError(ValueError):
    """
    This error is raised when the Google API complains -- for example, because
    it encounters a language it can't translate or transliterate.
    """
    pass

def _quote_text(text):
    """
    Represent text in a URL-safe form, even if it has slashes in it or is
    in Unicode.
    """
    if isinstance(text, unicode):
        text = text.encode('utf-8')
    return urllib.quote(text, safe='')

def _language_api_call(method, version, input, source_lang='', target_lang=''):
    """
    Make a REST/JSON call to the Google Language API.
    """
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
    if response['responseStatus'] == 200:
        return response['responseData']
    elif response['responseStatus'] == 400:
        raise RequestError(response['responseStatus'])
    else:
        raise urllib2.HTTPError(url, response['responseStatus'],
        response['responseDetails'], {}, None)

def translate(text, source_lang, target_lang):
    """
    Translate text from `source_lang` into `target_lang`.

    Both languages should be given as ISO 639 language codes.
    """
    response = _language_api_call('translate', '1.0', text, source_lang,
    target_lang)

    return response['translatedText']

def transliterate_word(word, source_lang, target_lang):
    """
    Transliterate (re-spell) a single word from `source_lang`
    to `target_lang`.
    
    Both languages should be given as ISO 639 language codes.
    """
    response = _language_api_call('transliterate', '1.0', word, source_lang,
    target_lang)
    return response['transliterations'][0]['transliteratedWords'][0]

def transliterate(text, source_lang, target_lang):
    """
    Transliterate (re-spell) text from `source_lang` to `target_lang`.
    
    Both languages should be given as ISO 639 language codes.
    """
    trans = []
    for word in tokenize_list(text):
        trans.append(transliterate_word(word, source_lang, target_lang))
    return untokenize_list(trans)

def english_name(lcode):
    try:
        return langs.english_name(lcode)
    except KeyError:
        return '<'+lcode+'>'

def detect_language(text, human_readable=False):
    """
    Detects what language the given text is in. Returns a tuple of
    (language, confidence).

    If `human_readable` is False, this returns an ISO 639 language code.
    If `human_readable` is True, this returns the English name of the language.
    """
    response = _language_api_call('detect', '1.0', text)
    if human_readable:
        return english_name(response['language']), response['confidence']
    else:
        return response['language'], response['confidence']

def auto_translate(text, target_lang):
    """
    Translates text from whatever language it's in to the target language.
    
    The language should be given as an ISO 639 language code.
    """
    source_lang, confidence = detect_language(text)
    return translate(text, source_lang, target_lang)

def to_english(text):
    """
    Translates anything to English!

    If it encounters a language that Google can't translate, it will at least
    tell you what language it was, as in (something in Sanskrit).
    """
    try:
        return auto_translate(text, 'en')
    except RequestError:
        lang, confidence = detect_language(text)
        try:
            trans = transliterate(text, lang, 'en')
            return '("%s" in %s)' % (trans, english_name(lang))
        except RequestError:
            return "(something in %s)" % english_name(lang)

def demo():
    print translate('hello world', 'en', 'ja')
    print transliterate('hello world', 'en', 'ru')
    print to_english(translate('hello world', 'en', 'ja'))
    print to_english(u"नमस्ते")

if __name__ == '__main__': demo()

