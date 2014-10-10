# -*- coding: UTF-8 -*-
# Created by ldconejo (luisconej@gmail.com)
# Reads a website in Mandarin and converts it to Pinyin with
# with hovering translations in English
# Version: 0.1
# Work in progress, no guarantees are provided
#************************************************************
# Dictionary
# CC-CEDICT
# Community maintained free Chinese-English dictionary.
#
# Published by MDBG
#
# License:
# Creative Commons Attribution-Share Alike 3.0
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Referenced works:
# CEDICT - Copyright (C) 1997, 1998 Paul Andrew Denisowski
#
# CC-CEDICT can be downloaded from:
# http://www.mdbg.net/chindict/chindict.php?page=cc-cedict
#
# Additions and corrections can be sent through:
# http://cc-cedict.org/editor/editor.php
#
# For more information about CC-CEDICT see:
# http://cc-cedict.org/wiki/
#
#! version=1
#! subversion=0
#! format=ts
#! charset=UTF-8
#! entries=110098
#! publisher=MDBG
#! license=http://creativecommons.org/licenses/by-sa/3.0/
#! date=2014-09-24T23:27:27Z
#! time=1411601247
#************************************************************

import urllib2
import re
import goslate
import sqlite3
import webbrowser
import os

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
# improveDic(cnChar)
# Makes modifications to the base Google translator-based dictionary, adding more elaborate definitions to
# hovering text.
#######################################################################################################################
def improveDic():
    dictFile = os.getcwd() + '/cedict_ts.u8'
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
        c.execute('UPDATE myDictionary SET pinyin=? WHERE chinese=?', (newDefinition, chinese))
        conn.commit()
        print "INFO: RECORD UPDATED: " + chinese + " " + newDefinition
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

#CHANGE THIS IN ORDER TO USE A DIFFERENT WEBSITE
response = urllib2.urlopen('http://www.bbc.co.uk/zhongwen/simp')

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

#Open output file in default browser
new = 2
url = 'file:///' + os.getcwd() + '/test.html'
print url
finalRes = webbrowser.open(url, new=new)
print finalRes
#improveDic()