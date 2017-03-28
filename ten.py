#encoding: utf-8
import urllib2
import time
import re
import datetime
from pprint import pprint
# from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup
# import tushare as ts
import MySQLdb

def getSoup (url) :
    times = 0
    while times < 10 :
        try :
            req = urllib2.Request(url)
            res = urllib2.urlopen(req, timeout = 15).read()
            # return BeautifulSoup(res, "html.parser")
            return BeautifulSoup(res,fromEncoding="gb18030")

        except :
            print "Could not get soup from " + url
            print "Sleep 3 seconds and retrying ..."
            time.sleep(3)
            times = times + 1

    return ""

def getPageInfo(url, page) :
    realURL = url + "&page=" + str(page)

    soup = getSoup(realURL)
    tbody = soup.find(attrs={'class':'datalist'}).table.tbody
    trArray = tbody.findAll("tr")
    numArray = tbody.findAll("script")

    for index, tr in enumerate(trArray) :
        record = {}
        td = tr.findAll("td")
        record['person']        = td[0].text.encode("utf8")
        record['name']          = td[3].text.encode("utf8")
        record['code']          = numArray[index * 2 + 1].text.encode("utf8")[13:19]
        record['price']         = td[6].text.encode("utf8")
        record['success']       = td[9].text.encode("utf8")

        if record['success'] == '--' :
            record['success'] = '0'

        dateAndTime = re.split('\s+', td[5].text.encode("utf8"))
        record['pdate'] = dateAndTime[0]
        record['ptime'] = dateAndTime[1]
        record['sdate'] = td[10].text.encode("utf8")

        # pprint(record)
        insertDB(record, "ten")
        # exit()

def insertDB(info, table) :
    print info['person'] + ":" + info['pdate'] + " " + info['ptime'] + ":" + info['name']

    cur = conn.cursor()

    statement = "insert into " + table + "(person,name,code,price,pdate,ptime,success,sdate) VALUES('" + info['person'] + "','" + \
        info['name'] + "','" + info['code'] + "','" + info['price'] + "','" + info['pdate'] + "','" + info['ptime'] + "','" + info['success'] + "','" + \
        info['sdate'] + "')"

    try :
        cur.execute(statement)
        cur.close()
        conn.commit()

    except MySQLdb.Error, e:
        print "\tMysql Error %d: %s" % (e.args[0], e.args[1])

host = "localhost"
user = "root"
passwd = "1qazxsw2"
port = 3306
database = "stock"

conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=database,port=port,charset='utf8')

tenURL = "http://www.178448.com/fjzt-1.html?view=archiver"
page = 1

while page <= 53689 :
    print "page:" + str(page)
    getPageInfo(tenURL, page)
    page = page + 1
