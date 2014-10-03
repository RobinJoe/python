import sys
from sh import bugzilla
from sh import sed

# --------------------------------------------------------------------------------
# Read and write functions

def readData(infile):
    try:
        with open(infile, 'rb') as f:
            info = f.read()
    except IOError as ioerr:
        print('File error (readData): ' + str(ioerr))
    return info

def writeData(info, outfile):
    try:
        with open(outfile, 'wb') as f:
            f.write(info)
    except IOError as ioerr:
        print('File error (writeData): ' + str(ioerr))

def extract():
    query = bugzilla('query', '--savedsearch=bugex', '-i', _out="buglist.txt")
    buglist = readData("buglist.txt").strip().split()
    doctext = readData("doctext.xml").strip().split("</varlistentry>")
    bugnum = 0
    chunknum = 0
    result = []

    for bug in buglist:
        bugnum += 1
        for chunk in doctext:
            if chunk.find(bug) > 0:
                chunknum += 1
                result.append(chunk + '</varlistentry>')

    result = ''.join(result)
    writeData(result, 'output.xml')
    print('Bugs:   ' + str(bugnum))
    print('Chunks: ' + str(chunknum))

# --------------------------------------------------------------------------------
# Main function

if __name__ == "__main__":
    extract()