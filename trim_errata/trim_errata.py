#!/usr/bin/python

def trim_errata():
    try:
        with open('errataData.txt', 'rb') as f:
            info = f.read()
    except IOError as ioerr:
        print('File error (errataData.txt): ' + str(ioerr))

    buglist = info.strip().split()
    trim_list = []
    count = 0

    for item in buglist:
        if item.startswith("#") and item[-1].isdigit():
            print(item)
            trim_list.append(item)
            count += 1
    print(count)

    result = '\n'.join(trim_list)
    try:
        with open('output.txt', 'wb') as f:
            f.write(result)
    except IOError as ioerr:
        print('File error (writeData): ' + str(ioerr))
    return

# --------------------------------------------------------------------------------
# Main function

if __name__ == "__main__":
    trim_errata()