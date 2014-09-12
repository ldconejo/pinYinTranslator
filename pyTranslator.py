# -*- coding: UTF-8 -*-
# Created by ldconejo
# Reads a website in Mandarin

import urllib2
import re
import goslate

#Proxy setup
proxy = urllib2.ProxyHandler({'http': 'proxy01.sc.intel.com:911'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)

#Proxy setup for translator
gs = goslate.Goslate(opener=opener)

response = urllib2.urlopen('http://www.xinhuanet.com/')

#for line in response.readlines():
#    line = unicode(line, 'utf-8')
#    for n in re.findall(ur'[\u4e00-\u9fff]', line):

        #Perform online translation
#        print "RESULT:" + n
#        english = gs.translate(n, 'en')
#        print "TRANSLATION:" + english

#gs_roman = goslate.Goslate(writing='WRITING_ROMAN',opener=opener)
WRITING_NATIVE_AND_ROMAN = (u'trans', u'translit')
gs_roman = goslate.Goslate(WRITING_NATIVE_AND_ROMAN, opener=opener)
result = gs_roman.translate("Dad", 'zh', )
print result[1]

