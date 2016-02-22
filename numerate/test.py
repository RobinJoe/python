#!/bin/python3
"""Test file for numerate.py."""

import logging

import numerate


# import pytest


def test_precleanxml():
    """Test precleanxml."""
    assert numerate.precleanxml(' ') == ' '
    assert numerate.precleanxml('o  o') == 'o o'
    assert numerate.precleanxml('o   o') == 'o o'


def test_postcleanxml():
    """Test postcleanxml."""
    assert numerate.postcleanxml('test') == 'test'
    assert numerate.postcleanxml("`") == "'"
    assert numerate.postcleanxml('C&U;') == 'C&amp;U'
    assert numerate.postcleanxml(' & ') == ' and '
    assert numerate.postcleanxml('\t') == ''
    assert numerate.postcleanxml('\t\t') == ''
    assert numerate.postcleanxml('\t\t\t') == ''
    assert numerate.postcleanxml('\n') == '\n'
    assert numerate.postcleanxml('\n\n') == '\n'
    assert numerate.postcleanxml('\n\n\n') == '\n'


def test_cleanxml():
    """Test cleanxml."""
    stringin = '''
<screen>
    BBB & CCC  C&U;  this ' and ` that code


        DDD & EEE  C&U;  this ' and ` that code
</screen>
'''

    stringout = '''
<screen>BBB and CCC C&amp;U this ' and ' that code
DDD and EEE C&amp;U this ' and ' that code</screen>
'''

    stringin = numerate.precleanxml(stringin)
    stringin = numerate.postcleanxml(stringin)
    assert stringin == stringout


# @pytest.mark.xfail
def test_reorderoutput():
    """Test reorderoutput."""
    filein = 'input.xml'
    stringout = readdata('output.xml')
    assert numerate.reorder(filein, False, False) == stringout


def readdata(infile):
    """Test readdata."""
    try:
        with open(infile, 'rb') as f:
            xml = f.read()
    except IOError as ioerr:
        logging.error('File error (readdata): ' + str(ioerr))
    return xml
