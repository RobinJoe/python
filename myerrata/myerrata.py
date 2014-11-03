#!/usr/bin/python2.7

import sh

num_to_display = int(raw_input('Number of bugs to display:  '))


def open_bugs():
    try:
        with open('errataData.txt', 'rb') as f:
            info = f.read()
    except IOError as ioerr:
        print('File error (readData): ' + str(ioerr))

    buglist = info.strip().split()
    more_bugs = 'y'

    while more_bugs == 'y':
        print('Opening the following bugs:')

        for i in range(num_to_display):
            print buglist[0]
            bug = 'https://bugzilla.redhat.com/show_bug.cgi?id=' + buglist.pop(0)
            sh.firefox(bug)
        response = raw_input('Remove completed bugs? (y/n):  ')

        if response == 'y':
            info = '\n'.join(buglist)
            try:
                with open('errataData.txt', 'wb') as f:
                    f.write(info)
            except IOError as ioerr:
                print('File error (writeData): ' + str(ioerr))
        more_bugs = raw_input('Open another batch of bugs? (y/n):  ')
    return

# --------------------------------------------------------------------------------
# Main function

if __name__ == "__main__":
    open_bugs()