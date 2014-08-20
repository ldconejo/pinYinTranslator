#!/usr/bin/env python
import re

#Parsing of dictionary source file
def readSourceFile():
    #Open dictionary file
    f = open('dictionarySource.html', 'r')
    for line in f:
        #print line
        #Check if the line contains a Unicode character matching the range of Chinese characters
        #result = re.match(".*htm.*",line)
        result = re.search(u'[\u00d8-\u00f6]', line)
        if result:
            result = re.findall(u'[\u00d8-\u00f6]', line)
            print result
            print line
        #print line

def main():
    print "Reading html file"
    readSourceFile()


if __name__ == '__main__':
    main()