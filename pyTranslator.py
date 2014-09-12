# -*- coding: UTF-8 -*-
# Created by ldconejo
# Reads a website in Mandarin

import urllib2
import re
import goslate
import sqlite3

#######################################################################################################################
# Database Functions
#######################################################################################################################

#######################################################################################################################
# initDatabase
# Creates the database if it does not exist
#######################################################################################################################

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

    #Perform online translation
    english = gs.translate(n, 'en')
    result = gs_roman.translate(n, 'zh', )
    return (english, result[1])

#Proxy setup
proxy = urllib2.ProxyHandler({'http': 'proxy01.sc.intel.com:911'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)

#Proxy setup for translator
gs = goslate.Goslate(opener=opener)
WRITING_NATIVE_AND_ROMAN = (u'trans', u'translit')
gs_roman = goslate.Goslate(WRITING_NATIVE_AND_ROMAN, opener=opener)

response = urllib2.urlopen('http://www.xinhuanet.com/')

for line in response.readlines():
    line = unicode(line, 'utf-8')
    for n in re.findall(ur'[\u4e00-\u9fff]', line):

        #Perform online translation
        result = searchInWeb(n)

        #Replace the character in the original line
        line = re.sub(n,result[1] + ' ',line)
    print line
