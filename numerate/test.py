import numerate
import logging
# import pytest


def test_precleanXML():
    assert numerate.precleanXML(' ') == ' '
    assert numerate.precleanXML('o  o') == 'o o'
    assert numerate.precleanXML('o   o') == 'o o'


def test_postcleanXML():
    assert numerate.postcleanXML('test') == 'test'
    assert numerate.postcleanXML("`") == "'"
    assert numerate.postcleanXML('C&U;') == 'C&amp;U'
    assert numerate.postcleanXML(' & ') == ' and '
    assert numerate.postcleanXML('\t') == ''
    assert numerate.postcleanXML('\t\t') == ''
    assert numerate.postcleanXML('\t\t\t') == ''
    assert numerate.postcleanXML('\n') == '\n'
    assert numerate.postcleanXML('\n\n') == '\n'
    assert numerate.postcleanXML('\n\n\n') == '\n'


def test_cleanXML():
    stringIN = '''
<screen>
    BBB & CCC  C&U;  this ' and ` that code


        DDD & EEE  C&U;  this ' and ` that code
</screen>
'''

    stringOUT = '''
<screen>BBB and CCC C&amp;U this ' and ' that code
DDD and EEE C&amp;U this ' and ' that code</screen>
'''

    stringIN = numerate.precleanXML(stringIN)
    stringIN = numerate.postcleanXML(stringIN)
    assert stringIN == stringOUT


# @pytest.mark.xfail


def test_reorderOutput():
    fileIN = 'input.xml'
    stringOUT = readData('output.xml')
    assert numerate.reorder(fileIN, False, False) == stringOUT

# ----------------------------------------------------------
# Helper functions


def readData(infile):  # reads XML from file
    try:
        with open(infile, 'rb') as f:
            xml = f.read()
    except IOError as ioerr:
        logging.error('File error (readData): ' + str(ioerr))
    return xml
