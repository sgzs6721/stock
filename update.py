#encoding: utf-8
import urllib2
import time
import re
import datetime
from pprint import pprint
from bs4 import BeautifulSoup
# from BeautifulSoup import BeautifulSoup

import MySQLdb

def getSoup (url) :
    times = 0
    while times < 10 :
        try :
            req = urllib2.Request(url)
            res = urllib2.urlopen(req, timeout = 15).read()
            return BeautifulSoup(res, "html.parser")
            # return BeautifulSoup(res,fromEncoding="gb18030")

        except :
            print "Could not get soup from " + url
            print "Sleep 3 seconds and retrying ..."
            time.sleep(3)
            times = times + 1

    return ""

def getPageInfo(url, page) :
    realURL = url + "page=" + str(page)

    soup = getSoup(realURL)
    tbody = soup.find(attrs={'class':'datalist'}).table.tbody
    trArray = tbody.findAll("tr")

    trArray.reverse()

    for index, tr in enumerate(trArray) :
        record = {}
        td = tr.findAll("td")
        record['person']        = td[0].text.encode("utf8")
        record['name']          = td[3].text.encode("utf8")
        record['price']         = td[6].text.encode("utf8")
        record['success']       = td[9].text.encode("utf8")

        if record['success'] == '--' :
            record['success'] = '0'

        dateAndTime = re.split('\s+', td[5].text.encode("utf8"))
        record['pdate'] = dateAndTime[0]

        record['ptime'] = dateAndTime[1]
        record['sdate'] = td[10].text.encode("utf8")

        print currentDate
        print record['sdate']

        if not record['sdate'] == currentDate :
            exit()
        updateDB(record, "ten")

def updateDB(info, table) :
    print info['person'] + ":" + info['pdate'] + " " + info['ptime'] + ":" + info['name']

    cur = conn.cursor()

    statisticTable = "statistics"

    update = "update `" + table + "` set success = success + 1,udate = '" + currentDate  + " where person = '" + info['person'] + \
             "' AND name = '" + info['name'] + "' pdate = '" + info['pdate'] + "' AND udate !='" + currentDate + "'"
    update2 = "update `" + statisticTable + "` set success = success + 1 where person ='" + info['person'] + "'"

    try :
        cur.execute(update)
        if info['success'] == 1 :
            cur.execute(update2)
        cur.close()
        conn.commit()

    except MySQLdb.Error, e:
        print "\tMysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()


host = "localhost"
user = "root"
passwd = "1qazxsw2"
port = 3306
database = "stock"

conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=database,port=port,charset='utf8')
currentDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# tenURL = "http://www.178448.com/fjzt-1.html?view=archiver&"
tenURL = "http://www.178448.com/fjzt-2.html?"
page = 1

while page >= 1 :
    print "page:" + str(page)
    getPageInfo(tenURL, page)
    page = page + 1
    exit()
