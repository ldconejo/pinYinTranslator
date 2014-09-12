# -*- coding: UTF-8 -*-
# Created by ldconejo
# Reads a website in Mandarin

import urllib2
import re

proxy = urllib2.ProxyHandler({''})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
response = urllib2.urlopen('http://www.xinhuanet.com/')

#p = re.compile('[\u4E00-\u9FA0]')


for line in response.readlines():
    print line
    #line = u'<title>新华网_传播中国 报道世界</title>'
    #line = u'%r' % line
    line = unicode(line, 'utf-8')
    for n in re.findall(ur'[\u4e00-\u9fff]+', line):
        print "RESULT:" + n
    #result = p.findall(line)
    #print unicode(result)


