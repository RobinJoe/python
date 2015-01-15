import pytest
import numerate

def test_precleanXML():
    assert numerate.precleanXML(' ') == ' '
    assert numerate.precleanXML('\n') == '\n'
    assert numerate.precleanXML('hello\n\nthere') == 'hello\nthere'
    assert numerate.precleanXML('\n\n\n') == '\n'
    assert numerate.precleanXML('\n\n\n\n') == '\n'

def test_postcleanXML():
    assert numerate.postcleanXML('test') == 'test'
    assert numerate.postcleanXML("`") == "'"
    assert numerate.postcleanXML('C&U;') == 'C&amp;U'
    assert numerate.postcleanXML(' & ') == ' and '

@pytest.mark.xfail
def test_reorderOutput():
    fileIN = 't_input.xml'
    stringOUT = readData('t_output.xml')
    assert numerate.reorder(fileIN, False, False) == stringOUT

#----------------------------------------------------------
# Helper functions

def readData(infile):  # reads XML from file
    try:
        with open(infile, 'rb') as f:
            xml = f.read()
    except IOError as ioerr:
        logging.error('File error (readData): ' + str(ioerr))
    return xml