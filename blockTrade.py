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
    realURL = url + str(page) + "/ajax/1"
    soup = getSoup(realURL)
    tbody = soup.table.tbody
    trArray = tbody.findAll("tr")
    trArray.reverse()

    for index, tr in enumerate(trArray) :
        record = {}
        td = tr.findAll("td")
        record['date']         = td[1].text.encode("utf8")
        record['code']         = td[2].text.encode("utf8")
        record['name']         = td[3].text.encode("utf8")
        record['close']        = td[4].text.encode("utf8")
        record['price']        = td[5].text.encode("utf8")
        record['vol']          = td[6].text.encode("utf8")
        record['discount']     = td[7].text.encode("utf8").split("%")[0]
        record['buy']          = td[8].text.encode("utf8")
        record['sell']         = td[9].text.encode("utf8")

        # pprint(record)
        # if not checkExistRecord(record, "blocktrade") :
        insertDB(record, "blocktrade")
        # exit()

def insertDB(info, table) :

    print info['name'] + "," + info['date'] + ","  + info['price'] + "," + info['discount']
    cur = conn.cursor()
    insertStatement = "insert into " + table + "(date,code,name,close,price,vol,discount,buy,sell) VALUES(\"" + info['date'] + "\",'" + \
        info['code'] + "','" + info['name'] + "','" + info['close'] + "','" + info['price'] + "','" + info['vol'] + "','" + \
        info['discount'] + "','" + info['buy'] + "','" + info['sell'] + "')"

    try :
        cur.execute(insertStatement)
        cur.close()
        conn.commit()

    except MySQLdb.Error, e:
        print "\tMysql Error %d: %s" % (e.args[0], e.args[1])


def checkExistRecord(record, table) :
    cur = conn.cursor()
    queryStatement = "select * from `" + table + "` where person = '" + record['person'] + "' AND name = '" + record['name'] + \
                     "' AND date = '" + record['date'] + "' AND price = '" + record['price'] + "'"

    try :
        cur.execute(queryStatement)
        info = cur.fetchall()
        # pprint(info)
        if len(info) :
            return True
    except :
        print "select error!"
        exit(1)

    return False

host = "localhost"
user = "root"
passwd = "1qazxsw2"
port = 3306
database = "stock"

conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=database,port=port,charset='utf8')

ggmmURL = "http://data.10jqka.com.cn/market/dzjy/field/enddate/order/desc/page/"
page = 1

while page > 0 :
    print "page:" + str(page)
    getPageInfo(ggmmURL, page)
    page = page - 1
