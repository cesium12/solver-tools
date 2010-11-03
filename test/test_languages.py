from solvertools.model.language_model import *

def test_latin():
    latin_model = get_model('la')
    assert latin_model.text_goodness('SEMPER UBI SUB UBI') == latin_model.text_goodness('SEMPER VBJ SUB VBJ')
    assert latin_model.text_goodness('LOREMIPSUM') > latin_model.text_goodness('MANICSAGES')
    assert latin_model.split_words('mensetmanvs')[0] == 'mens et manvs'

def test_chaotic():
    chaotic_model = get_model('chaos')
    assert (chaotic_model.split_words('wumdinmoldinpanzosti')[0] ==
            'wum din moldin panzosti')
    assert (chaotic_model.split_words('unteam')[0] ==
            'unte am')
    

