#encoding: utf-8
import urllib2
import re
import datetime
import time
import math
from pprint import pprint
from bs4 import BeautifulSoup
# from BeautifulSoup import BeautifulSoup
import tushare as ts
import MySQLdb

def getSoup (url) :
    times = 0
    while times < 10 :
        try :
            req = urllib2.Request(url)
            res = urllib2.urlopen(req, timeout = 15).read()
            return BeautifulSoup(res, "html.parser",from_encoding="gb18030")
            # return BeautifulSoup(res,from_encoding="gb18030")

        except :
            print "Could not get soup from " + url
            print "Sleep 3 seconds and retrying ..."
            time.sleep(3)
            times = times + 1

    return ""

def getPageInfo(url, page) :
    soup = getSoup(url)
    tbody = soup.findAll("table")[9].findAll("tbody")[1]
    trArray = tbody.findAll("tr")

    for index, tr in enumerate(trArray) :
        record = {}
        td = tr.findAll("td")
        record['date']         = td[1].text.encode("utf8")
        number = td[2].text.encode("utf8").split(" ")
        record['first']        = number[0]
        record['second']       = number[1]
        record['third']        = number[2]
        record['fourth']       = number[3]
        record['last']         = number[4]

        insertDB(record, "11x5")
        # exit()

def insertDB(info, table) :

    print info['date'] + "," + info['first'] + ","  + info['second'] + "," + info['third'] + "," + info['fourth'] + "," + info['last']
    cur = conn.cursor()
    insertStatement = "insert into " + table + "(dateNo,first,second,third,fourth,last) VALUES(\"" + info['date'] + "\",'" + \
        info['first'] + "','" + info['second'] + "','" + info['third'] + "','" + info['fourth'] + "','" + info['last'] + "')"

    try :
        cur.execute(insertStatement)
        cur.close()
        conn.commit()

    except MySQLdb.Error, e:
        print "\tMysql Error %d: %s" % (e.args[0], e.args[1])
        exit(1)

def getDate(dateNoStr) :
    dateNo = datetime.datetime.strptime(dateNoStr, "%Y%m%d")
    addDate = dateNo + datetime.timedelta(days=1)
    return addDate.strftime("%Y%m%d")

host = "localhost"
user = "root"
passwd = "1qazxsw2"
port = 3306
database = "stock"

conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=database,port=port,charset='utf8')

ggmmURL = "http://zst.cjcp.com.cn/cjw11x5_qs/view/11x5_jiben-5-bj11x5-11-1-"
pageDate = "20141105"

while pageDate != "20170809" :
    print "pageDate:" + str(pageDate)
    page = pageDate + "01-" + pageDate + "99-9.html"
    getPageInfo(ggmmURL+page, page)
    pageDate = getDate(pageDate)
    # exit()
