import numerate

def test_cleanXML():
    assert numerate.cleanXML('<screen>\n') == '<screen>'
    assert numerate.cleanXML('test') == 'test'
    assert numerate.cleanXML("`") == "'"
    assert numerate.cleanXML('C&U') == 'C&amp;U'
    assert numerate.cleanXML(' & ') == ' and '
    assert numerate.cleanXML(' #<') == ' &lt;'

def test_cleanXML_para():
    assert numerate.cleanXML('') == ''