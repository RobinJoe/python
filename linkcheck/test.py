import pytest
import linkcheck

def test_precleanXML():
    assert numerate.precleanXML(' ') == ' '

#@pytest.mark.xfail
#def test_reorderOutput():
#    fileIN = 'input.xml'
#    stringOUT = readData('output.xml')
#    assert numerate.reorder(fileIN, False, False) == stringOUT

#----------------------------------------------------------
# Helper functions

def readData(infile):  # reads XML from file
    try:
        with open(infile, 'rb') as f:
            xml = f.read()
    except IOError as ioerr:
        logging.error('File error (readData): ' + str(ioerr))
    return xml