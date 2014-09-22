# -*- coding: UTF-8 -*-
# Created by ldconejo
# Reads a website in Mandarin

import urllib2
import re
import goslate
import sqlite3
import webbrowser

#######################################################################################################################
# Database Functions
#######################################################################################################################

#######################################################################################################################
# initDatabase
# Creates the database if it does not exist
#######################################################################################################################
def initDatabase():
    c.execute('''CREATE TABLE myDictionary
             (chinese, pinyin, translation)''')

#######################################################################################################################
# addRecord
# Adds a new record to the database
#######################################################################################################################
def addRecord(chinese, pinyin, translation):
    result = c.execute("""INSERT INTO myDictionary(chinese, translation, pinyin) VALUES (?, ?, ?)""",
                       (chinese, translation, pinyin))
    conn.commit()
    return result
#######################################################################################################################
# searchRecord
# Searches a record in the database
#######################################################################################################################
def searchRecord(chinese):
    c.execute('SELECT * FROM myDictionary WHERE chinese=?', chinese)

    result = c.fetchone()

    #If word is unknown, then do a web search
    if str(result) == "None":
        translation = searchInWeb(chinese)
        addRecord(chinese, translation[0], translation[1])
        c.execute('SELECT * FROM myDictionary')
        return (translation[0], translation[1])
    else:
        return (result[1], result[2])

#######################################################################################################################
# searchWord(Chinese_Character)
# Searches the character in the database. If it is not found, uses the Google Translate API to get the relevant
# information and updates the database.
# Returns a list with the word in Pinyin and the English translation
#######################################################################################################################

#######################################################################################################################
# searchInWeb(cnChar)
# Uses the Google Translate API to obtain the Pinyin word and English translation of a Chinese character
#######################################################################################################################
def searchInWeb(cnChar):
    gs = goslate.Goslate()
    WRITING_NATIVE_AND_ROMAN = (u'trans', u'translit')
    gs_roman = goslate.Goslate(WRITING_NATIVE_AND_ROMAN)

    #Perform online translation
    english = gs.translate(n, 'en')
    result = gs_roman.translate(n, 'zh', )
    return (english, result[1])

#######################################################################################################################
# MAIN FLOW
#######################################################################################################################
#Start database
conn = sqlite3.connect('pyTranslator.db')
c = conn.cursor()
try:
    initDatabase()
except:
    pass

WRITING_NATIVE_AND_ROMAN = (u'trans', u'translit')

gs_roman = goslate.Goslate(WRITING_NATIVE_AND_ROMAN)

response = urllib2.urlopen('http://news.xinhuanet.com/health/2014-09/17/c_126994624.htm')

#Create a new file to store the output
workfile = '/Users/luisconejo/Desktop/test.html'
f = open(workfile, 'w+')

for line in response.readlines():
    #print line
    line = unicode(line, 'utf-8')
    for n in re.findall(ur'[\u4e00-\u9fff]', line):

        #Perform online translation
        result = searchRecord(n)

        finalLine = "<span title=\"" + result[0] + "\">" + result[1] + "</span>"

        #Replace the character in the original line
        line = re.sub(n,finalLine + ' ',line)

    f.write(line.encode("UTF-8"))
    #print line

#Close output file
print "INFO: Conversion completed"
f.close()

#Open output file in default browser
new = 2
url = 'file:///Users/luisconejo/Desktop/test.html'
webbrowser.open(url,new=new)