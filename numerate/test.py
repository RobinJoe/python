import numerate

def test_cleanXML():
    assert numerate.cleanXML('<screen>\n') == '<screen>'
    assert numerate.cleanXML('<screen>\t') == '<screen>'
    assert numerate.cleanXML('test') == 'test'
    assert numerate.cleanXML("`") == "'"
    assert numerate.cleanXML('C&U') == 'C&amp;U'
    assert numerate.cleanXML(' & ') == ' and '
    assert numerate.cleanXML(' ') == ' '
    assert numerate.cleanXML('\n') == '\n'
    assert numerate.cleanXML('hello\n\nthere') == 'hello\nthere'
    assert numerate.cleanXML('\n\n\n') == '\n'
    assert numerate.cleanXML('\n\n\n\n') == '\n'

#def test_cleanXML_para():
#    stringIN = readData('input.xml')
#    stringOUT = readData('output.xml')
#    assert numerate.cleanXML(stringIN) == stringOUT

def test_reorderOutput():
    fileIN = 'input.xml'
    stringOUT = readData('output.xml')
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