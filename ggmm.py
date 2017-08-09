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
    # trArray.reverse()

    for index, tr in enumerate(trArray) :
        record = {}
        td = tr.findAll("td")
        record['code']         = td[1].text.encode("utf8")
        record['name']         = td[2].text.encode("utf8")
        record['person']       = td[3].text.encode("utf8")
        record['date']         = td[4].text.encode("utf8")
        record['number']       = td[5].text.encode("utf8")
        record['price']        = td[6].text.encode("utf8")
        record['type']         = td[7].text.encode("utf8")
        record['executives']   = td[10].text.encode("utf8")
        record['position']     = td[12].text.encode("utf8")
        record['relation']     = td[13].text.encode("utf8")


        detail = ts.get_hist_data(record['code'], start=record['date'])
        df = detail.iloc[::-1]
        close = df[u"close"][0]
        record['close'] = str(close)

        m = re.match(r"([0-9.-]+)(\xe4\xb8\x87)?", record['number'])
        if record['price'] != "--" :
            money = float(m.groups()[0]) * float(record['price'])
            if m.groups()[1] != None :
                money *= 10000
            record['money'] = str(money / 10000)
            record['discount'] =  str(round((float(record['price']) - close) / close * 100, 2))
        else :
            record['price'] = '0'
            record['money'] = '0'
            record['discount'] = '0'

        # pprint(record)
        # if not checkExistRecord(record, "ggmm") :
        insertDB(record, "ggmm")

def insertDB(info, table) :

    print info['name'] + "','" + info['person'] + "','" + info['date'] + "','" + info['number'] + "','" + info['price']
    cur = conn.cursor()
    insertStatement = "insert into " + table + "(code,name,person,date,number,price,type,executives,position,relation,close,money,discount) VALUES(\"" + info['code'] + "\",'" + \
        info['name'] + "','" + info['person'] + "','" + info['date'] + "','" + info['number'] + "','" + info['price'] + "','" + \
        info['type'] + "','" + info['executives'] + "','" + info['position'] + "','" + info['relation'] + "','" +info['close'] + "','" +  info['money'] + "','" + info['discount'] + "')"

    try :
        cur.execute(insertStatement)
        cur.close()
        conn.commit()

    except MySQLdb.Error, e:
        print "\tMysql Error %d: %s" % (e.args[0], e.args[1])
        exit(0)


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

ggmmURL = "http://data.10jqka.com.cn/financial/ggjy/field/enddate/order/desc/page/"
page = 1

while page > 0 :
    print "page:" + str(page)
    insertNum = getPageInfo(ggmmURL, page)
    if insertNum == 50 :
        page = page + 1
