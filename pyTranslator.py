# -*- coding: UTF-8 -*-
# Created by ldconejo
# Reads a website in Mandarin

import urllib2
import re
import goslate
import sqlite3
import webbrowser
import os
import time

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

    #Proxy setup for translator
    gs = goslate.Goslate(opener=opener)
    WRITING_NATIVE_AND_ROMAN = (u'trans', u'translit')
    gs_roman = goslate.Goslate(WRITING_NATIVE_AND_ROMAN, opener=opener)

    #gs = goslate.Goslate()
    #WRITING_NATIVE_AND_ROMAN = (u'trans', u'translit')
    #gs_roman = goslate.Goslate(WRITING_NATIVE_AND_ROMAN)

    #Perform online translation
    english = gs.translate(n, 'en')
    result = gs_roman.translate(n, 'zh', )
    return (english, result[1])

#######################################################################################################################
# improveDic(cnChar)
# Makes modifications to the base Google translator-based dictionary, adding more elaborate definitions to
# hovering text.
#######################################################################################################################
def improveDic():
    #dictFile = '/Users/luisconejo/Desktop/cedict_1_0_ts_utf-8_mdbg.txt'
    dictFile = os.getcwd() + '\cedict_ts.u8'
    pinyinDict = open(dictFile, 'r')
    #dictLine = pinyinDict.read

    for dictLine in pinyinDict.readlines():
        #Look for lone character in line
        dictLine = unicode(dictLine, 'utf-8')
        for character in re.findall(ur'\s[\u4e00-\u9fff]\s', dictLine):
            #print character
            #Now, get the definition for the character
            for definition in re.findall(ur'/.*/', dictLine):
                definition = re.sub(ur'[//|<|>|\u4e00-\u9fff]', '\n', definition)
                updateRecord(character[1], definition)
                pass
                #print definition
#######################################################################################################################
# updateRecord
# Updates a record in the database
#######################################################################################################################
def updateRecord(chinese, newDefinition):
    c.execute('SELECT * FROM myDictionary WHERE chinese=?', chinese)
    #c.execute('SELECT * FROM myDictionary')
    result = c.fetchone()

    #If word is unknown, then ignore
    if str(result) == "None":
        print "NO MATCH"
    else:
        if(result[0] == chinese)and(result[1] != newDefinition):
            print "RESULT: " + result[0] + result[1]
            try:
                c.execute('UPDATE myDictionary SET pinyin=? WHERE chinese=?', (newDefinition, chinese))
                conn.commit()
            except:
                pass
            print "INFO: RECORD UPDATED: " + chinese + " " + newDefinition
        #time.sleep(1)
    result = None

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

#Proxy setup
proxy = urllib2.ProxyHandler({'http': 'proxy01.sc.intel.com:911'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)

#Proxy setup for translator
gs = goslate.Goslate(opener=opener)
WRITING_NATIVE_AND_ROMAN = (u'trans', u'translit')
gs_roman = goslate.Goslate(WRITING_NATIVE_AND_ROMAN, opener=opener)

WRITING_NATIVE_AND_ROMAN = (u'trans', u'translit')

gs_roman = goslate.Goslate(WRITING_NATIVE_AND_ROMAN)

response = urllib2.urlopen('http://www.bbc.co.uk/zhongwen/simp')
#response = urllib2.urlopen('http://chinesereadingpractice.com/2013/08/05/mr-pigs-picnic/')

#Create a new file to store the output
workfile = 'test.html'
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
        #print line

    f.write(line.encode("UTF-8"))
    print line

#Close output file
print "INFO: Conversion completed"
f.close()

#Get current work directory
currentDir = os.getcwd()

#Convert to web format
currentDir = re.sub(r'([\\])', '/', currentDir)
print "CURRENT DIR:" + currentDir

#Open output file in default browser
new = 2
url = 'file:///' + currentDir + '/test.html'

webbrowser.open(url,new=new)

#improveDic()